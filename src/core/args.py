from argparse import ArgumentParser
from pathlib import Path


def parse_args():
    # TODO: json_file present dans le main et redéfini ici ????? import le la variable depuis le main avec une variable CONSTANTE ???
    json_file = "input_parameters.json"
    src_folder = Path(__file__).absolute().parents[1]

    parser = ArgumentParser()

    parser.add_argument(
        "-p",
        "--parameters",
        type=Path,
        default=src_folder.joinpath("resources"),
        help="Path of the parameters.json folder.\nDEFAULT: folder containing a default input_parameters.json file",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path.cwd(),
        help="Path folder to save results files.\nDEFAULT: current working directory",
    )
    return parser.parse_args()
