import pytest
import random

from src.models.library import Library
from src.models.locus import Locus


@pytest.fixture
def setup():
    #SetUp simply library without locus, seq_probe
    library_empty = Library(chromosome_name='ch3L',
                      start_lib=8500,
                      nbr_loci_total=5,
                      max_diff_percent=10,
                      design_type="locus_length")

    # design sequence randomly with coordinates
    start_seq = list(range(8000, 80000, 50))
    end_seq = list(range(8030, 80030, 50))
    seq = [''.join(random.choices(['a', 't', 'g', 'c'], k=30)) for _ in range(len(start_seq))]
    seq_list = []
    for start, end, seq in zip(start_seq, end_seq, seq):
        seq_list.append([start, end, seq])

    # SetUp library with locus and seq_probe
    library_with_loci = Library(chromosome_name='ch3L',
                            start_lib=8500,
                            nbr_loci_total=5,
                            max_diff_percent=10,
                            design_type="locus_length")
    seq1 = [8733, 8763, 'GATAGATAGCATCATCATCTACTATCATCTATCAT']
    locus1 = Locus(['BB297.Fw', 'GACTGGTACTCGCGTGACTTG', 'BB299.Rev', 'CCAGTCCAGAGGTGTCCCTAC'])
    locus1.seq_probe = [x[2] for x in seq_list[:30]]
    locus2 = Locus(['BB297.Fw', 'GACTGGTACTCGCGTGACTTG', 'BB299.Rev', 'CCAGTCCAGAGGTGTCCCTAC'])
    locus2.seq_probe = [x[2] for x in seq_list[30:60]]
    locus2.seq_probe.append(seq1[2])
    library_with_loci.add_locus(locus1)
    library_with_loci.add_locus(locus2)

    return seq_list, library_empty, library_with_loci


def test_reduce_list_seq_type_locus_length(setup):
    sequences, library, _ = setup
    library.design_type = "locus_length"
    seq_list_reduced = library.reduce_list_seq(sequences,
                                               resolution=1000,
                                               nbr_probe_by_locus=20)
    assert len(seq_list_reduced) == 100


def test_reduce_list_seq_type_nbr_probes(setup):
    sequences, library, _ = setup
    library.design_type = "nbr_probes"
    seq_list_reduced = library.reduce_list_seq(sequences,
                                               resolution=1000,
                                               nbr_probe_by_locus=30)
    assert len(seq_list_reduced) == 150


def test_check_length_seq_diff_check_returns_values(setup):
    sequences, _, library_with_loci = setup
    min, max, diff_bp, diff_percent = library_with_loci.check_length_seq_diff()
    assert (min == 30
            and max == 35
            and diff_bp == 5
            and diff_percent == 14.285714285714292)

def test_completion_without_threshold_exceeded(setup, capsys):
    sequences, _, library_with_loci = setup
    library_with_loci.max_diff_percent=20
    library_with_loci.completion(14, 35)
    captured_stdout = capsys.readouterr().out
    assert captured_stdout == '-'*70+'\n'+'No completion required\n'+'-'*70+'\n'

def test_completion_with_threshold_exceeded(setup, capsys):
    sequences, _, library_with_loci = setup
    library_with_loci.completion(14, 135)
    captured_stdout = capsys.readouterr().out
    assert captured_stdout == '-' * 70 + '\n' + 'Completion finished\n' + '-' * 70 + '\n'