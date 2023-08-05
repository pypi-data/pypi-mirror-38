from argparse import ArgumentParser, FileType, Namespace

from facenet_sandberg.config import ValidateConfig

from evaluator.evaluator import Evaluator
from metrics.metrics import DistanceMetric, ThresholdMetric


def _parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--config_file',
                        type=str,
                        required=True,
                        help='Path to the config file')
    parser.add_argument('--image_dir',
                        type=str,
                        required=True,
                        help='Path to the image directory.')
    parser.add_argument('--pairs_file_name',
                        type=str,
                        required=True,
                        help='Filename of pairs.txt')
    parser.add_argument('--model_path',
                        type=str,
                        required=True,
                        help='Path to the facial recognition model')
    parser.add_argument(
        '--is_insightface',
        action='store_true',
        help='Set this flag if the model is insightface')
    parser.add_argument(
        '--prealigned_flag',
        action='store_true',
        help='Specify if the images have already been aligned.')
    return parser.parse_args()


def validate(
        config_file: str,
        image_dir: str,
        pairs_file_name: str,
        model_path: str,
        is_insightface: bool,
        prealigned_flag: bool) -> None:
    config = ValidateConfig(
        config_file,
        image_dir,
        pairs_file_name,
        model_path,
        is_insightface,
        prealigned_flag)
    evaluator = Evaluator.create_evaluator(config)
    evaluation_results = evaluator.evaluate()
    print('Evaluation results: ', evaluation_results)
    parser_metrics = evaluator.compute_metrics()
    print('Parser metrics: ', parser_metrics)


def cli() -> None:
    args = _parse_arguments()
    validate(
        args.config_file,
        args.image_dir,
        args.pairs_file_name,
        args.model_path,
        args.is_insightface,
        args.prealigned_flag,
    )


if __name__ == '__main__':
    cli()
