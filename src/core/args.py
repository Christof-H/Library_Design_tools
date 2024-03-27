import argparse
from argparse import ArgumentParser
from pathlib import Path


def check_args(arguments: argparse.ArgumentParser) -> None:
    if not arguments.parameters.parent.exists():
        raise SystemExit(
            f"Input parameters file folder ({arguments.parameters.parent.as_posix()}): INVALID FOLDER."
        )
    if not arguments.parameters.is_file():
        raise SystemExit(
            f"Input parameters file ({arguments.parameters.name}): FILE NOT FOUND."
        )
    if not arguments.output.exists():
        raise SystemExit(
            f"Output folder ({arguments.output.as_posix()}): INVALID FOLDER."
        )


def parse_args() -> argparse.ArgumentParser:
    src_folder = Path(__file__).absolute().parents[1]
    params_file_path = src_folder.joinpath("resources", "input_parameters.json")

    parser = ArgumentParser()

    parser.add_argument(
        "-p",
        "--parameters",
        type=Path,
        default=params_file_path,
        help="Path of the parameters.json file.\nDEFAULT: default input_parameters.json file",
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