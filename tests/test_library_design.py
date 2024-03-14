import pytest
import os
import copy
import json
import re
import datetime as dt

import src.modules.data_function as df
from src.models.library import Library
from src.models.locus import Locus


@pytest.fixture(scope="session")
def setup(tmp_path_factory):
    test_folder = os.path.dirname(os.path.realpath(__file__))
    script_folder = os.path.abspath(os.path.join(test_folder, ".."))

    primer_univ_file = "Primer_univ.csv"
    resources_path = script_folder + os.sep + "src" + os.sep + "resources"
    primer_univ_path = resources_path + os.sep + primer_univ_file
    result_folder = tmp_path_factory.mktemp("Library_Design_Results")

    dic = {"test_folder": test_folder, "script_folder": script_folder}

    input_param_folder = [
        "resources/design_by_length_bcd/IN/input_parameters.json",
        "resources/design_by_length_rt/IN/input_parameters.json",
        "resources/design_by_probe_nbr_bcd/IN/input_parameters.json",
        "resources/design_by_probe_nbr_rt/IN/input_parameters.json",
    ]
    for json_path in input_param_folder:
        full_path = test_folder + os.sep + json_path
        input_parameters = df.load_parameters(full_path)

        input_parameters["end_lib"] = input_parameters["start_lib"] + (
            input_parameters["nbr_loci_total"] * input_parameters["resolution"]
        )

        bcd_rt_path = resources_path + os.sep + input_parameters["bcd_rt_file"]
        genomic_path = (
            input_parameters["chromosome_folder"]
            + os.sep
            + input_parameters["chromosome_file"]
        )

        bcd_rt_list = df.bcd_rt_format(bcd_rt_path)
        list_seq_genomic = df.seq_genomic_format(genomic_path)
        primer_univ_list = df.universal_primer_format(primer_univ_path)

        primer = [
            primer_univ_list[key]
            for key, values in primer_univ_list.items()
            if key == input_parameters["primer_univ"]
        ]
        primer = primer[0]

        library = Library(input_parameters)

        list_seq_genomic_reduced = library.reduce_list_seq(
            list_seq_genomic,
            resolution=input_parameters["resolution"],
            nbr_probe_by_locus=input_parameters["nbr_probe_by_locus"],
        )

        # Filling the Library class with all the Locus
        for i in range(1, library.nbr_loci_total + 1):
            locus = Locus(
                primers_univ=primer,
                locus_n=i,
                chr_name=library.chromosome_name,
                resolution=input_parameters["resolution"],
                nbr_probe_by_locus=input_parameters["nbr_probe_by_locus"],
                design_type=input_parameters["design_type"],
            )
            list_seq, start, end = locus.recover_genomic_seq(
                i,
                input_parameters["nbr_loci_total"],
                input_parameters["start_lib"],
                list_seq_genomic_reduced,
            )
            locus.start_seq = start
            locus.end_seq = end
            locus.seq_probe = list_seq
            library.add_locus(locus)

        # Sequences for barcodes/RTs added to primary probes according to locus
        library.add_rt_bcd_to_primary_seq(bcd_rt_list, input_parameters)

        # Sequences for universal primers added to the primary probes at each end
        library.add_univ_primer_each_side()

        # Checking primary probes length for all Locus
        min_length, max_length, diff_nbr, diff_percentage = (
            library.check_length_seq_diff()
        )
        library.completion(diff_percentage, max_length)

        result_regex = re.search(r"design(\w+)/", json_path)
        name_design = "lib" + result_regex.group(1)
        folder_name = name_design + "_path"
        path_result_folder = result_folder / name_design
        path_result_folder.mkdir()

        dic[folder_name] = path_result_folder
        dic[name_design] = library

    return dic


def test_summary_locus_length_with_bcd(setup):
    path_result_folder = setup["lib_by_length_bcd_path"]
    library = setup["lib_by_length_bcd"]
    path_output = setup["test_folder"] + os.sep + "resources/design_by_length_bcd/OUT"
    summary_test = path_result_folder / "3_Library_summary.csv"
    summary_output_reference = path_output + os.sep + "3_Library_summary.csv"

    df.library_summary_file(path_result_folder, library)

    # Opening and comparing the initial results files with the new files generated for the test
    with open(summary_output_reference, mode="r", encoding="UTF-8") as reference_file:
        reference_text = reference_file.read()
        with open(summary_test, mode="r", encoding="UTF-8") as test_file:
            test_text = test_file.read()
            assert len(reference_text) == len(test_text)


def test_summary_locus_length_with_rt(setup):
    path_result_folder = setup["lib_by_length_rt_path"]
    library = setup["lib_by_length_rt"]
    path_output = setup["test_folder"] + os.sep + "resources/design_by_length_rt/OUT"
    summary_test = path_result_folder / "3_Library_summary.csv"
    summary_output_reference = path_output + os.sep + "3_Library_summary.csv"

    df.library_summary_file(path_result_folder, library)

    # Opening and comparing the initial results files with the new files generated for the test
    with open(summary_output_reference, mode="r", encoding="UTF-8") as reference_file:
        reference_text = reference_file.read()
        with open(summary_test, mode="r", encoding="UTF-8") as test_file:
            test_text = test_file.read()
            assert len(reference_text) == len(test_text)


def test_summary_locus_nbr_probe_with_bcd(setup):
    path_result_folder = setup["lib_by_probe_nbr_bcd_path"]
    library = setup["lib_by_probe_nbr_bcd"]
    path_output = (
        setup["test_folder"] + os.sep + "resources/design_by_probe_nbr_bcd/OUT"
    )
    summary_test = path_result_folder / "3_Library_summary.csv"
    summary_output_reference = path_output + os.sep + "3_Library_summary.csv"

    df.library_summary_file(path_result_folder, library)

    # Opening and comparing the initial results files with the new files generated for the test
    with open(summary_output_reference, mode="r", encoding="UTF-8") as reference_file:
        reference_text = reference_file.read()
        with open(summary_test, mode="r", encoding="UTF-8") as test_file:
            test_text = test_file.read()
            assert len(reference_text) == len(test_text)


def test_summary_locus_nbr_probe_with_rt(setup):
    path_result_folder = setup["lib_by_probe_nbr_rt_path"]
    library = setup["lib_by_probe_nbr_rt"]
    path_output = setup["test_folder"] + os.sep + "resources/design_by_probe_nbr_rt/OUT"
    summary_test = path_result_folder / "3_Library_summary.csv"
    summary_output_reference = path_output + os.sep + "3_Library_summary.csv"

    df.library_summary_file(path_result_folder, library)

    # Opening and comparing the initial results files with the new files generated for the test
    with open(summary_output_reference, mode="r", encoding="UTF-8") as reference_file:
        reference_text = reference_file.read()
        with open(summary_test, mode="r", encoding="UTF-8") as test_file:
            test_text = test_file.read()
            assert len(reference_text) == len(test_text)