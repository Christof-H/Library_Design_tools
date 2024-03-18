import os

import pytest
import random

from models.locus import Locus


@pytest.fixture
def locus():
    primer_univ = [
        "BB297.Fw",
        "GACTGGTACTCGCGTGACTTG",
        "BB299.Rev",
        "CCAGTCCAGAGGTGTCCCTAC",
    ]
    locus = Locus(resolution=20000, nbr_probe_by_locus=100, primers_univ=primer_univ)
    return locus


@pytest.fixture
def sequences():
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


def test_recover_genomic_seq_locus_length_strategy(locus, sequences):
    locus.design_type = "locus_length"
    final_seq, start, end = locus.recover_genomic_seq(2, 3, 10000, sequences)
    assert len(final_seq) == 100 and start == 30000 and end == 50000


def test_recover_genomic_seq_nbr_probes_strategy(locus, sequences):
    locus.design_type = "nbr_probes"
    final_seq, start, end = locus.recover_genomic_seq(2, 3, 10000, sequences)
    assert len(final_seq) == 100 and start == 13000 and end == 17980


def test_check_nbr_probes_overtaking(locus, sequences):
    seq_list = sequences[:400]
    assert len(locus.check_nbr_probes(seq_list)) == locus.nbr_probe_by_locus
