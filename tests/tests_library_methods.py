import pytest
import random

from src.models.library import Library


@pytest.fixture
def sequences():
    start_seq = list(range(8000, 80000, 50))
    end_seq = list(range(8030, 80030, 50))
    seq = [''.join(random.choices(['a', 't', 'g', 'c'], k=30)) for _ in range(len(start_seq))]
    seq_list = []
    for start, end, seq in zip(start_seq, end_seq, seq):
        seq_list.append([start, end, seq])
    return seq_list


def test_reduce_list_seq_type_locus_length(sequences):
    library = Library(chromosome_name='ch3L',
                      start_lib=8500,
                      nbr_loci_total=5,
                      max_diff_percent=10,
                      design_type="locus_length")
    seq_list_reduced = library.reduce_list_seq(sequences,
                                               resolution=1000,
                                               nbr_probe_by_locus=20)
    assert len(seq_list_reduced) == 100


def test_reduce_list_seq_type_nbr_probes(sequences):
    library = Library(chromosome_name='ch3L',
                      start_lib=8500,
                      nbr_loci_total=6,
                      max_diff_percent=10,
                      design_type="nbr_probes")
    seq_list_reduced = library.reduce_list_seq(sequences,
                                               resolution=1000,
                                               nbr_probe_by_locus=20)
    assert len(seq_list_reduced) == 120
