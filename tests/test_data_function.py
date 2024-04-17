import pytest
import os
from pathlib import Path
import core.data_function as df


@pytest.fixture
def file_path():
    """Set up paths to find the various RT files, Barcodes, universal primers and genomic sequences"""
    test_folder = Path(__file__).absolute().parent
    script_folder = test_folder.parent
    dic_path = {}
    dic_path["rt_file_path"] = script_folder.joinpath("src/resources/List_RT.csv")
    dic_path["bcd_file_path"] = script_folder.joinpath("src/resources/Barcodes.csv")
    dic_path["univ_primer"] = script_folder.joinpath("src/resources/Primer_univ.csv")
    dic_path["exemple_genomic_seq"] = test_folder.joinpath("resources/chr3L.bed")
    return dic_path


def test_bcd_rt_format_rt_output(file_path):
    """Test whether the list of RTs corresponds to the expected shape and list of RTs"""
    expected_output_rt_0 = ["revMer1", "caccgacgtcgcatagaacg"]
    expected_output_rt_last = ["revMer6", "ttggaggtgtagggagtaaa"]
    list_bcd_rt = df.bcd_rt_format(file_path["rt_file_path"])
    assert list_bcd_rt[0] == expected_output_rt_0
    assert list_bcd_rt[-1] == expected_output_rt_last
    assert len(list_bcd_rt) == 35


def test_bcd_rt_format_bcd_output(file_path):
    """Test whether the list of RTs corresponds to the expected shape and list of barcodes"""
    expected_output_bcd_0 = ["Bcd_001", "GCTATCGTTCGTTCGAGGCC"]
    expected_output_bcd_last = ["Bcd_199", "tcaagcgtgtcggcgttgcg"]
    list_bcd_rt = df.bcd_rt_format(file_path["bcd_file_path"])
    assert list_bcd_rt[0] == expected_output_bcd_0
    assert list_bcd_rt[-1] == expected_output_bcd_last
    assert len(list_bcd_rt) == 195


def test_universal_primer_format_output(file_path):
    """Test whether the list of universal primers corresponds to the expected shape and list of universal primers"""
    expected_output_univ_primer_1 = [
        "BB297.Fw",
        "GACTGGTACTCGCGTGACTTG",
        "BB299.Rev",
        "CCAGTCCAGAGGTGTCCCTAC",
    ]
    output_univ_primer = df.universal_primer_format(file_path["univ_primer"])
    output_univ_primer_1 = output_univ_primer.get("primer1")
    assert expected_output_univ_primer_1 == output_univ_primer_1
    assert len(output_univ_primer) == 8


def test_seq_genomic_format_output_type(file_path):
    """Test whether the list of genomic probes corresponds to the expected shape and list of genomic probes"""
    seq_genomic_output_0 = df.seq_genomic_format(file_path["exemple_genomic_seq"])[0]
    assert isinstance(seq_genomic_output_0, list)
    assert isinstance(seq_genomic_output_0[0], int)
    assert isinstance(seq_genomic_output_0[1], int)
    assert isinstance(seq_genomic_output_0[2], str)
