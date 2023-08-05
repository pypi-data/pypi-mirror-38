import logging
from os.path import isfile, join
from parser.pair import Pair
from parser.parser_base import ParserBase
from typing import Dict, Iterable


class PairParser(ParserBase):

    def __init__(self, pairs_fname: str, image_dir: str) -> None:
        self.pairs_fname = pairs_fname
        self._image_dir = image_dir

    def compute_pairs(self) -> Iterable[Pair]:
        with open(self.pairs_fname, 'r', encoding='utf-8') as f:
            next(f)  # pylint: disable=stop-iteration-return
            # skip first line, which contains metadata
            for line in f:
                try:
                    pair = self._compute_pair(line)
                except FileNotFoundError:
                    logging.exception('Skipping invalid file')
                else:
                    yield pair

    def compute_metrics(self) -> Dict[str, float]:
        raise NotImplementedError()

    def _compute_full_path(self, image_path: str) -> str:
        exts = ['.jpg', '.png']
        for ext in exts:
            full_image_path = join(self._image_dir, '{}{}'.format(image_path, ext))
            if isfile(full_image_path):
                return full_image_path
        err = '{} does not exist with extensions: {}'.format(image_path, exts)
        raise FileNotFoundError(err)

    def _compute_pair(self, line: str) -> Pair:
        line_info = line.strip().split()
        if len(line_info) == 3:
            name, n1, n2 = line_info
            image1 = self._compute_full_path(join(name,
                                                  '{}_{}'.format(name, "%04d" % int(n1))))
            image2 = self._compute_full_path(join(name,
                                                  '{}_{}'.format(name, "%04d" % int(n2))))
            is_match = True
        else:
            name1, n1, name2, n2 = line_info
            image1 = self._compute_full_path(join(name1,
                                                  '{}_{}'.format(name1, "%04d" % int(n1))))
            image2 = self._compute_full_path(join(name2,
                                                  '{}_{}'.format(name2, "%04d" % int(n2))))
            is_match = False
        return Pair(image1, image2, is_match)
