import argparse
from argparse import ArgumentParser
from pathlib import Path


def check_args(arguments: argparse.ArgumentParser) -> None:
    if not arguments.parameters.exists():
        raise SystemExit(
            f"Input parameters file folder ({arguments.parameters.as_posix()}): INVALID."
        )
    if not arguments.output.exists():
        raise SystemExit(f"Output folder ({arguments.output.as_posix()}): INVALID.")


def parse_args():
    # TODO: src_folder present dans le main et redéfini ici ????? import le la variable depuis le main avec une variable CONSTANTE ???
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
    check_args(parser.parse_args())

    return parser.parse_args()
