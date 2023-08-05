"""Face Detection and Recognition"""

import itertools
import os
import pickle
from glob import glob, iglob
from typing import Dict, Generator, List
from urllib.request import urlopen

import cv2
import numpy as np
import tensorflow as tf
from facenet_sandberg import facenet, validate_on_lfw
from facenet_sandberg.align import align_dataset_mtcnn
from mtcnn.mtcnn import MTCNN
from scipy import misc

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)


class Face:
    """Class representing a single face

    Attributes:
        name {str} -- Name of person
        bounding_box {Float[]} -- box around their face in container_image
        image {Image} -- Image cropped around face
        container_image {Image} -- Original image
        embedding {Float} -- Face embedding
        matches {Matches[]} -- List of matches to the face
        url {str} -- Url where image came from
    """

    def __init__(self):
        self.name: str = None
        self.bounding_box: List[float] = None
        self.image: Image = None
        self.container_image: Image = None
        self.embedding: Embedding = None
        self.matches: List[Match] = []
        self.url: str = None


class Match:
    """Class representing a match between two faces

    Attributes:
        face_1 {Face} -- Face object for person 1
        face_2 {Face} -- Face object for person 2
        score {Float} -- Distance between two face embeddings
        is_match {bool} -- whether is match between faces
    """

    def __init__(self):
        self.face_1: Face = Face()
        self.face_2: Face = Face()
        self.score: float = float("inf")
        self.is_match: bool = False


Image = np.ndarray
Embedding = np.ndarray
EmbeddingsGenerator = Generator[List[Embedding], None, None]
ImageGenerator = Generator[Image, None, None]
FacesGenerator = Generator[List[Face], None, None]


class Identifier:
    """Class to detect, encode, and match faces

    Arguments:
        threshold {Float} -- Distance threshold to determine matches
    """

    def __init__(self, model_checkpoint: str,
                 threshold: float = 1.10, is_insightface: bool=False, dropout_rate: float=0.1):
        self.detector = Detector()
        if is_insightface:
            self.encoder = InsightFace(
                model_fp=model_checkpoint,
                dropout_rate=dropout_rate)
        else:
            self.encoder = Facenet(model_checkpoint)
        self.threshold: float = threshold

    @staticmethod
    def download_image(url: str) -> Image:
        req = urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        image = cv2.imdecode(arr, -1)
        return Identifier.fix_image(image)

    @staticmethod
    def get_image_from_path(image_path: str) -> Image:
        return Identifier.fix_image(cv2.imread(image_path))

    @staticmethod
    def get_images_from_dir(
            directory: str, recursive: bool) -> ImageGenerator:
        if recursive:
            image_paths = iglob(os.path.join(
                directory, '**', '*.*'), recursive=recursive)
        else:
            image_paths = iglob(os.path.join(directory, '*.*'))
        for image_path in image_paths:
            yield Identifier.fix_image(cv2.imread(image_path))

    @staticmethod
    def fix_image(image: Image):
        if image.ndim < 2:
            image = image[:, :, np.newaxis]
        if image.ndim == 2:
            image = facenet.to_rgb(image)
        image = image[:, :, 0:3]
        return image

    def vectorize(self, image: Image,
                  prealigned: bool = False,
                  detect_multiple_faces: bool=True,
                  face_limit: int = 5) -> List[Embedding]:
        """Gets face embeddings in a single image
        Keyword Arguments:
            prealigned {bool} -- is the image already aligned
            face_limit {int} -- max number of faces allowed
                                before image is discarded. (default: {5})

        """
        if not prealigned:
            faces = self.detect_encode(
                image, detect_multiple_faces, face_limit)
            vectors = [face.embedding for face in faces]
        else:
            vectors = [self.encoder.generate_embedding(image)]
        return vectors

    def vectorize_all(self,
                      images: ImageGenerator,
                      prealigned: bool = False,
                      detect_multiple_faces: bool=True,
                      face_limit: int = 5) -> List[List[Embedding]]:
        """Gets face embeddings from a generator of images
        Keyword Arguments:
            prealigned {bool} -- is the image already aligned
            face_limit {int} -- max number of faces allowed
                                before image is discarded. (default: {5})
        """
        vectors = []
        if not prealigned:
            all_faces = self.detect_encode_all(
                images=images,
                save_memory=True,
                detect_multiple_faces=detect_multiple_faces,
                face_limit=face_limit)
            for faces in all_faces:
                vectors.append([face.embedding for face in faces])
        else:
            embeddings = self.encoder.generate_embeddings(images)
            for embedding in embeddings:
                vectors.append([embedding])
        return vectors

    def detect_encode(self, image: Image,
                      detect_multiple_faces: bool=True,
                      face_limit: int=5) -> List[Face]:
        """Detects faces in an image and encodes them
        """

        faces = self.detector.find_faces(
            image, detect_multiple_faces, face_limit)
        for face in faces:
            face.embedding = self.encoder.generate_embedding(face.image)
        return faces

    def detect_encode_all(self,
                          images: ImageGenerator,
                          urls: [str]=None,
                          save_memory: bool=False,
                          detect_multiple_faces: bool=True,
                          face_limit: int=5) -> FacesGenerator:
        """For a list of images finds and encodes all faces

        Keyword Arguments:
            save_memory {bool} -- Saves memory by deleting image from Face objects.
                                Should only be used if with you have some other kind
                                of refference to the original image like a url. (default: {False})
        """

        all_faces = self.detector.bulk_find_face(
            images, urls, detect_multiple_faces, face_limit)
        return self.encoder.get_face_embeddings(all_faces, save_memory)

    def compare_embedding(self,
                          embedding_1: Embedding,
                          embedding_2: Embedding,
                          distance_metric: int=0) -> (bool,
                                                      float):
        """Compares the distance between two embeddings

        Keyword Arguments:
            distance_metric {int} -- 0 for Euclidian distance and 1 for Cosine similarity (default: {0})

        """

        distance = self.encoder.get_distance(embedding_1, embedding_2)
        is_match = False
        if distance < self.threshold:
            is_match = True
        return is_match, distance

    def compare_images(self, image_1: Image, image_2: Image,
                       detect_multiple_faces: bool=True, face_limit: int=5) -> Match:
        match = Match()
        image_1_faces = self.detect_encode(
            image_1, detect_multiple_faces, face_limit)
        image_2_faces = self.detect_encode(
            image_2, detect_multiple_faces, face_limit)
        if image_1_faces and image_2_faces:
            for face_1 in image_1_faces:
                for face_2 in image_2_faces:
                    distance = facenet.distance(face_1.embedding.reshape(
                        1, -1), face_2.embedding.reshape(1, -1), distance_metric=0)[0]
                    if distance < match.score:
                        match.score = distance
                        match.face_1 = face_1
                        match.face_2 = face_2
            if distance < self.threshold:
                match.is_match = True
        return match

    def find_all_matches(self, image_directory: str,
                         recursive: bool) -> List[Match]:
        """Finds all matches in a directory of images
        """

        all_images = self.get_images_from_dir(image_directory, recursive)
        all_matches = []
        all_faces_lists = self.detect_encode_all(all_images)
        all_faces: Generator[Face, None, None] = (
            face for faces in all_faces_lists for face in faces)
        # Really inefficient way to check all combinations
        for face_1, face_2 in itertools.combinations(all_faces, 2):
            is_match, score = self.compare_embedding(
                face_1.embedding, face_2.embedding)
            if is_match:
                match = Match()
                match.face_1 = face_1
                match.face_2 = face_2
                match.is_match = True
                match.score = score
                all_matches.append(match)
                face_1.matches.append(match)
                face_2.matches.append(match)
        return all_matches

    def tear_down(self):
        self.encoder.tear_down()


class Facenet:
    def __init__(self, facenet_model_checkpoint: str):
        import tensorflow as tf
        self.sess = tf.Session()
        with self.sess.as_default():
            facenet.load_model(facenet_model_checkpoint)
        # Get input and output tensors
        self.images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        self.embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        self.phase_train_placeholder = tf.get_default_graph(
        ).get_tensor_by_name("phase_train:0")

    def generate_embedding(self, image: Image) -> Embedding:
        prewhiten_face = facenet.prewhiten(image)

        # Run forward pass to calculate embeddings
        feed_dict = {self.images_placeholder: [
            prewhiten_face], self.phase_train_placeholder: False}
        return self.sess.run(self.embeddings, feed_dict=feed_dict)[0]

    def generate_embeddings(self,
                            all_images: ImageGenerator) -> List[Embedding]:
        prewhitened_images = [
            facenet.prewhiten(image) for image in all_images]
        if prewhitened_images:
            feed_dict = {self.images_placeholder: prewhitened_images,
                         self.phase_train_placeholder: False}
            embeddings_array = self.sess.run(
                self.embeddings, feed_dict=feed_dict)
            embeddings = [embedding for embedding in embeddings_array]
            return embeddings
        return []

    def get_face_embeddings(self,
                            all_faces: FacesGenerator,
                            save_memory: bool=False) -> FacesGenerator:
        """Generates embeddings from generator of Faces
        Keyword Arguments:
            save_memory -- save memory by deleting image from Face object  (default: {False})
        """
        face_list = list(all_faces)
        prewhitened_images = [
            facenet.prewhiten(
                face.image) for faces in face_list for face in faces]
        if face_list:
            feed_dict = {self.images_placeholder: prewhitened_images,
                         self.phase_train_placeholder: False}
            embed_array = self.sess.run(self.embeddings, feed_dict=feed_dict)
            index = 0
            for faces in face_list:
                for face in faces:
                    if save_memory:
                        face.image = None
                        face.container_image = None
                    face.embedding = embed_array[index]
                    index += 1
                yield faces

    def get_best_match(self, anchor: Face,
                       faces: List[Face], save_memory: bool=False):
        anchor.embedding = self.generate_embedding(anchor.image)
        min_dist = float('inf')
        min_face = None
        for face in faces:
            face.embedding = self.generate_embedding(face.image)
            dist = self.get_distance(anchor.embedding, face.embedding)
            if dist < min_dist:
                min_dist = dist
                min_face = face
        return min_face

    @staticmethod
    def get_distance(embedding_1: Embedding,
                     embedding_2: Embedding,
                     distance_metric: int=0) -> float:
        """Compares the distance between two embeddings

        Keyword Arguments:
            distance_metric {int} -- 0 for Euclidian distance and 1 for Cosine similarity (default: {0})

        """

        distance = facenet.distance(embedding_1.reshape(
            1, -1), embedding_2.reshape(1, -1), distance_metric=distance_metric)[0]
        return distance

    def tear_down(self):
        self.sess.close()
        self.sess = None


class InsightFace(object):
    session = None
    graph = None
    output_ops = []
    input_ops = []
    feed_dict = {}

    def __init__(self, model_fp, device: str='/cpu:0', dropout_rate: float=0.1,
                 frozen=True, image_size: int=112):
        import tensorflow as tf
        self.model_fp = model_fp
        self.dropout_rate = dropout_rate
        self.input_tensor_names = ['img_inputs:0', 'dropout_rate:0']
        self.output_tensor_names = ['resnet_v1_50/E_BN2/Identity:0']
        self.frozen = frozen
        self.image_size = (image_size, image_size)

        with tf.device(device):
            self._load_graph()
            self._init_predictor()

    def _load_graph(self):
        if self.frozen:
            self._load_frozen_graph()
        else:
            self._restore_from_ckpt()

    def _restore_from_ckpt(self):
        self.saver = tf.train.Saver()
        self.saver.restore(self.session, self.model_fp)

    def _load_frozen_graph(self):
        self.graph = tf.Graph()
        with self.graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.model_fp, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        tf.get_default_graph()

    def _init_predictor(self):
        tf_config = tf.ConfigProto()
        tf_config.gpu_options.allow_growth = True
        with self.graph.as_default():
            self.session = tf.Session(config=tf_config, graph=self.graph)
            self._fetch_tensors()

    def _fetch_tensors(self):
        assert len(self.input_tensor_names) > 0
        assert len(self.output_tensor_names) > 0
        for _tensor_name in self.input_tensor_names:
            _op = self.graph.get_tensor_by_name(_tensor_name)
            self.input_ops.append(_op)
            self.feed_dict[_op] = None
        for _tensor_name in self.output_tensor_names:
            _op = self.graph.get_tensor_by_name(_tensor_name)
            self.output_ops.append(_op)

    def _set_feed_dict(self, data):
        assert len(data) == len(self.input_ops)
        with self.graph.as_default():
            for ind, op in enumerate(self.input_ops):
                self.feed_dict[op] = data[ind]

    def _clean_image(self, image: Image) -> np.ndarray:
        clean_image = cv2.resize(image, self.image_size)
        return clean_image

    def generate_embedding(self, image: Image) -> Embedding:
        clean_image = self._clean_image(image)
        input_data = [np.expand_dims(clean_image, axis=0), self.dropout_rate]
        with self.graph.as_default():
            self._set_feed_dict(data=input_data)
            embedding = self.session.run(
                self.output_ops, feed_dict=self.feed_dict)
        return np.reshape(embedding[0], -1)

    def generate_embeddings(self,
                            all_images: ImageGenerator) -> List[Embedding]:
        images = [self._clean_image(image) for image in all_images]
        input_data = [np.asarray(images), self.dropout_rate]
        if images:
            with self.graph.as_default():
                self._set_feed_dict(data=input_data)
                embeddings_array = self.session.run(
                    self.output_ops, feed_dict=self.feed_dict)[0]
                embeddings = [embedding for embedding in embeddings_array]
            return embeddings
        return []

    def get_face_embeddings(self,
                            all_faces: FacesGenerator,
                            save_memory: bool=False) -> FacesGenerator:
        """Generates embeddings from generator of Faces
        Keyword Arguments:
            save_memory -- save memory by deleting image from Face object  (default: {False})
        """
        face_list = list(all_faces)
        images = [self._clean_image(face.image)
                  for faces in face_list for face in faces]
        if len(images) > 1:
            input_data = [np.asarray(images), self.dropout_rate]
        elif len(images) == 1:
            input_data = [np.expand_dims(images[0], axis=0), self.dropout_rate]
        if face_list and images:
            with self.graph.as_default():
                self._set_feed_dict(data=input_data)
                embeddings_array = self.session.run(
                    self.output_ops, feed_dict=self.feed_dict)[0]
                index = 0
                for faces in face_list:
                    for face in faces:
                        if save_memory:
                            face.image = None
                            face.container_image = None
                        face.embedding = embeddings_array[index]
                        index += 1
                    yield faces

    @staticmethod
    def get_distance(embedding_1: Embedding,
                     embedding_2: Embedding,
                     distance_metric: int=0) -> float:
        """Compares the distance between two embeddings

        Keyword Arguments:
            distance_metric {int} -- 0 for Euclidian distance and 1 for Cosine similarity (default: {0})

        """

        distance = facenet.distance(embedding_1.reshape(
            1, -1), embedding_2.reshape(1, -1), distance_metric=distance_metric)[0]
        return distance

    def tear_down(self):
        self.session.close()
        tf.reset_default_graph()
        self.session = None
        self.graph = None


class Detector:
    # face detection parameters
    def __init__(
        self,
        face_crop_size: int=160,
        face_crop_margin: int=32,
        detect_multiple_faces: bool=True,
        min_face_size: int=20,
        scale_factor: float=0.709,
        steps_threshold: List[float]=[
            0.6,
            0.7,
            0.7]):
        self.detector = MTCNN(
            weights_file=None,
            min_face_size=min_face_size,
            steps_threshold=steps_threshold,
            scale_factor=scale_factor)
        self.face_crop_size = face_crop_size
        self.face_crop_margin = face_crop_margin
        self.detect_multiple_faces = detect_multiple_faces

    def bulk_find_face(self,
                       images: ImageGenerator,
                       urls: List[str] = None,
                       detect_multiple_faces: bool=True,
                       face_limit: int=5) -> FacesGenerator:
        for index, image in enumerate(images):
            faces = self.find_faces(image, detect_multiple_faces, face_limit)
            if urls and index < len(urls):
                for face in faces:
                    face.url = urls[index]
                yield faces
            else:
                yield faces

    def find_faces(self, image: Image, detect_multiple_faces: bool=True,
                   face_limit: int=5) -> List[Face]:
        faces = []
        results = self.detector.detect_faces(image)
        img_size = np.asarray(image.shape)[0:2]
        if len(results) < face_limit:
            if not detect_multiple_faces:
                results = results[:1]
            for result in results:
                face = Face()
                # bb[x, y, dx, dy]
                bb = result['box']
                bb = self.fit_bounding_box(
                    img_size[0], img_size[1], bb[0], bb[1], bb[2], bb[3])
                cropped = image[bb[1]:bb[3], bb[0]:bb[2], :]

                bb[0] = np.maximum(bb[0] - self.face_crop_margin / 2, 0)
                bb[1] = np.maximum(bb[1] - self.face_crop_margin / 2, 0)
                bb[2] = np.minimum(
                    bb[2] + self.face_crop_margin / 2, img_size[1])
                bb[3] = np.minimum(
                    bb[3] + self.face_crop_margin / 2, img_size[0])

                face.bounding_box = bb
                face.image = misc.imresize(
                    cropped, (self.face_crop_size, self.face_crop_size), interp='bilinear')

                faces.append(face)
        return faces

    @staticmethod
    def fit_bounding_box(max_x: int, max_y: int, x1: int,
                         y1: int, dx: int, dy: int) -> List[int]:
        x2 = x1 + dx
        y2 = y1 + dy
        x1 = max(min(x1, max_x), 0)
        x2 = max(min(x2, max_x), 0)
        y1 = max(min(y1, max_y), 0)
        y2 = max(min(y2, max_y), 0)
        return [x1, y1, x2, y2]


def align_dataset(
        input_dir,
        output_dir,
        image_size=182,
        margin=44,
        random_order=False,
        detect_multiple_faces=False):
    align_dataset_mtcnn.main(
        input_dir,
        output_dir,
        image_size,
        margin,
        random_order,
        detect_multiple_faces)


def test_dataset(
        lfw_dir,
        model,
        lfw_pairs,
        use_flipped_images,
        subtract_mean,
        use_fixed_image_standardization,
        image_size=160,
        lfw_nrof_folds=10,
        distance_metric=0,
        lfw_batch_size=128):
    validate_on_lfw.main(
        lfw_dir,
        model,
        lfw_pairs,
        use_flipped_images,
        subtract_mean,
        use_fixed_image_standardization,
        image_size,
        lfw_nrof_folds,
        distance_metric,
        lfw_batch_size)
