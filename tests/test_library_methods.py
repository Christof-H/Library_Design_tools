import pytest
import random

from models.library import Library
from models.locus import Locus


@pytest.fixture
def parameters():
    # Set parameters for Library instantiation
    parameters = {
        "chromosome_file": "chr3L.bed",
        "start_lib": 8500,
        "nbr_loci_total": 5,
        "max_diff_percent": 10,
        "design_type": "locus_length",
    }
    return parameters


@pytest.fixture
def sequences():
    # design seq_probe sequences randomly with coordinates
    start_seq = list(range(8000, 80000, 50))
    end_seq = list(range(8030, 80030, 50))
    seq = [
        "".join(random.choices(["a", "t", "g", "c"], k=30))
        for _ in range(len(start_seq))
    ]
    seq_list = []
    for start, end, seq in zip(start_seq, end_seq, seq):
        seq_list.append([start, end, seq])
    return seq_list


@pytest.fixture
def library_empty(parameters):
    # Set simply library without locus, seq_probe
    return Library(parameters)


@pytest.fixture
def library_filled(parameters, sequences):
    # Set library with locus and seq_probe
    library = Library(parameters)

    seq1 = [8733, 8763, "GATAGATAGCATCATCATCTACTATCATCTATCAT"]
    locus1 = Locus(
        ["BB297.Fw", "GACTGGTACTCGCGTGACTTG", "BB299.Rev", "CCAGTCCAGAGGTGTCCCTAC"]
    )
    locus1.seq_probe = [x[2] for x in sequences[:30]]
    locus2 = Locus(
        ["BB297.Fw", "GACTGGTACTCGCGTGACTTG", "BB299.Rev", "CCAGTCCAGAGGTGTCCCTAC"]
    )
    locus2.seq_probe = [x[2] for x in sequences[30:60]]
    locus2.seq_probe.append(seq1[2])
    library.add_locus(locus1)
    library.add_locus(locus2)
    return library


def test_reduce_list_seq_type_locus_length(sequences, library_empty):
    library_empty.design_type = "locus_length"
    seq_list_reduced = library_empty.reduce_list_seq(
        sequences, resolution=1000, nbr_probe_by_locus=20
    )
    assert len(seq_list_reduced) == 100


def test_reduce_list_seq_type_nbr_probes(sequences, library_filled):
    library_filled.design_type = "nbr_probes"
    seq_list_reduced = library_filled.reduce_list_seq(
        sequences, resolution=1000, nbr_probe_by_locus=30
    )
    assert len(seq_list_reduced) == 150


def test_check_length_seq_diff_check_returns_values(sequences, library_filled):
    min, max, diff_bp, diff_percent = library_filled.check_length_seq_diff()
    assert (
        min == 30 and max == 35 and diff_bp == 5 and diff_percent == 14.285714285714292
    )


def test_completion_without_threshold_exceeded(sequences, library_filled, capsys):
    library_filled.max_diff_percent = 20
    library_filled.completion(14, 35)
    captured_stdout = capsys.readouterr().out
    assert (
        captured_stdout
        == "-" * 70 + "\n" + "No completion required\n" + "-" * 70 + "\n"
    )


def test_completion_with_threshold_exceeded(sequences, library_filled, capsys):
    library_filled.completion(14, 135)
    captured_stdout = capsys.readouterr().out
    assert (
        captured_stdout == "-" * 70 + "\n" + "Completion finished\n" + "-" * 70 + "\n"
    )
