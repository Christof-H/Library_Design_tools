import pytest

from pathlib import Path
from src.core.args import parse_arguments, check_args


def test_check_param_bad_folder():
    wrong_folder_param_arg = parse_arguments(["-p", "folder/not/exist/input"])
    with pytest.raises(SystemExit, match=r".*folder/not/exist.*"):
        check_args(wrong_folder_param_arg)


def test_check_param_no_parameters_file():
    str_test_folder = (
        Path(__file__).absolute().parent.joinpath("input_parameters.json").as_posix()
    )
    no_file_param_arg = parse_arguments(["-p", str_test_folder])
    with pytest.raises(SystemExit, match=r".*input_parameters.json.*"):
        check_args(no_file_param_arg)


def test_check_param_bad_output_folder():
    wrong_output_folder = parse_arguments(["-o", "path/not/exist/output"])
    with pytest.raises(SystemExit, match=r".*path/not/exist/output.*"):
        check_args(wrong_output_folder)
