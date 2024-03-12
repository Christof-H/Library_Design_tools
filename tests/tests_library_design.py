import pytest
import os
import copy
import json
import re
import datetime as dt

import src.modules.data_import_function as data
from src.models.library import Library
from src.models.locus import Locus


@pytest.fixture(scope="session")
def setup(tmp_path_factory):
    test_folder = os.path.dirname(os.path.realpath(__file__))
    script_folder = os.path.abspath(os.path.join(test_folder, ".."))
    dic = {}
    primer_univ_file = "Primer_univ.csv"
    input_param_folder = ["./resources/design_by_length_bcd/IN/input_parameters.json",
                          "./resources/design_by_length_rt/IN/input_parameters.json",
                          "./resources/design_by_probe_nbr_bcd/IN/input_parameters.json",
                          "./resources/design_by_probe_nbr_rt/IN/input_parameters.json"]
    for json_path in input_param_folder:
        with open(json_path, mode="r", encoding="UTF-8") as file:
            input_parameters = json.load(file)

        chromosome_file = input_parameters["chromosome_file"]
        chromosome_folder = input_parameters["chromosome_folder"]
        resolution = input_parameters["resolution"]
        start_lib = input_parameters["start_lib"]
        nbr_loci_total = input_parameters["nbr_loci_total"]
        nbr_probe_by_locus = input_parameters["nbr_probe_by_locus"]
        nbr_bcd_rt_by_probe = input_parameters["nbr_bcd_rt_by_probe"]
        primer_univ = input_parameters["primer_univ"]
        bcd_rt_file = input_parameters["bcd_rt_file"]
        max_diff_percent = input_parameters["max_diff_percent"]
        design_type = input_parameters["design_type"]
        end_lib = start_lib + (nbr_loci_total * resolution)

        resources_path = script_folder + os.sep + "src" + os.sep + "resources"
        bcd_rt_path = resources_path + os.sep + bcd_rt_file
        genomic_path = chromosome_folder + os.sep + chromosome_file
        primer_univ_path = resources_path + os.sep + primer_univ_file

        result_folder = tmp_path_factory.mktemp("Library_Design_Results")

        bcd_rt_list = data.bcd_rt_format(bcd_rt_path)
        list_seq_genomic = data.seq_genomic_format(genomic_path)
        primer_univ_list = data.universal_primer_format(primer_univ_path)

        primer = [primer_univ_list[key] for key, values in primer_univ_list.items() if key == primer_univ]
        primer = primer[0]

        library = Library(
            chromosome_name=chromosome_file.split(".")[0],
            start_lib=start_lib,
            nbr_loci_total=nbr_loci_total,
            max_diff_percent=max_diff_percent,
            design_type=design_type
        )

        list_seq_genomic_reduced = library.reduce_list_seq(list_seq_genomic,
                                                           resolution=resolution,
                                                           nbr_probe_by_locus=nbr_probe_by_locus)

        # Filling the Library class with all the Locus
        for i in range(1, library.nbr_loci_total + 1):
            locus = Locus(primers_univ=primer, locus_n=i,
                          chr_name=library.chromosome_name,
                          resolution=resolution,
                          nbr_probe_by_locus=nbr_probe_by_locus,
                          design_type=design_type
                          )
            list_seq, start, end = locus.recover_genomic_seq(i,
                                                             nbr_loci_total,
                                                             start_lib,
                                                             list_seq_genomic_reduced)
            locus.start_seq = start
            locus.end_seq = end
            # locus.primers_univ=primer,
            locus.seq_probe = list_seq
            library.add_locus(locus)

        # Sequences for barcodes/RTs added to primary probes according to locus
        count = 0
        for locus in library.loci_list:
            seq_with_bcd = []
            bcd_rt_seq = bcd_rt_list[count][1]
            locus.bcd_locus = bcd_rt_list[count][0]

            for genomic_seq in locus.seq_probe:
                if nbr_bcd_rt_by_probe == 2:
                    seq_with_bcd.append(f"{bcd_rt_seq} {genomic_seq} {bcd_rt_seq}")
                elif nbr_bcd_rt_by_probe == 3:
                    seq_with_bcd.append(f"{bcd_rt_seq} {genomic_seq} {bcd_rt_seq * 2}")
                elif nbr_bcd_rt_by_probe == 4:
                    seq_with_bcd.append(f"{bcd_rt_seq * 2} {genomic_seq} {bcd_rt_seq * 2}")
                elif nbr_bcd_rt_by_probe == 5:
                    seq_with_bcd.append(f"{bcd_rt_seq * 3} {genomic_seq} {bcd_rt_seq * 2}")
            count += 1
            locus.seq_probe = seq_with_bcd

        # Sequences for universal primers added to the primary probes at each end

        for locus in library.loci_list:
            p_fw = copy.deepcopy(locus.primers_univ[1])
            p_rev = copy.deepcopy(locus.primers_univ[3])
            temp = [f"{p_fw} {x} {p_rev}" for x in locus.seq_probe]
            locus.seq_probe = temp

        min_length, max_length, diff_nbr, diff_percentage = library.check_length_seq_diff()
        library.completion(diff_percentage, max_length)

        result_regex = re.search(r'design(\w+)/', json_path)
        name_design = 'lib' + result_regex.group(1)
        folder_name = name_design + '_path'
        path_result_folder = result_folder / name_design
        path_result_folder.mkdir()

        dic[folder_name] = path_result_folder
        dic[name_design] = library

    return dic


def test_summary_locus_length_with_bcd(setup):
    path_result_folder = setup['lib_by_length_bcd_path']
    library = setup['lib_by_length_bcd']
    path_output = "resources/design_by_length_bcd/OUT"
    summary_test = path_result_folder / "3_Library_summary.csv"
    summary_output_reference = path_output + os.sep + "3_Library_summary.csv"

    with open(summary_test, mode="w", encoding="UTF-8") as file:
        file.write("Chromosome,Locus_N°,Start,End,Region size, Barcode,PU.Fw,PU.Rev,Nbr_Probes\n")
        for locus in library.loci_list:
            file.write(
                f"{locus.chr_name},{locus.locus_n},{locus.start_seq},\
{locus.end_seq},{locus.end_seq - locus.start_seq},{locus.bcd_locus},{locus.primers_univ[0]},\
{locus.primers_univ[2]},{len(locus.seq_probe)}\n"
            )

    with open(summary_output_reference, mode='r', encoding='UTF-8') as reference_file:
        reference_text = reference_file.read()
        with open(summary_test, mode='r', encoding='UTF-8') as test_file:
            test_text = test_file.read()
            assert len(reference_text) == len(test_text)


def test_summary_locus_length_with_rt(setup):
    path_result_folder = setup['lib_by_length_rt_path']
    library = setup['lib_by_length_rt']
    path_output = "resources/design_by_length_rt/OUT"
    summary_test = path_result_folder / "3_Library_summary.csv"
    summary_output_reference = path_output + os.sep + "3_Library_summary.csv"

    with open(summary_test, mode="w", encoding="UTF-8") as file:
        file.write("Chromosome,Locus_N°,Start,End,Region size, Barcode,PU.Fw,PU.Rev,Nbr_Probes\n")
        for locus in library.loci_list:
            file.write(
                f"{locus.chr_name},{locus.locus_n},{locus.start_seq},\
{locus.end_seq},{locus.end_seq - locus.start_seq},{locus.bcd_locus},{locus.primers_univ[0]},\
{locus.primers_univ[2]},{len(locus.seq_probe)}\n"
            )

    with open(summary_output_reference, mode='r', encoding='UTF-8') as reference_file:
        reference_text = reference_file.read()
        with open(summary_test, mode='r', encoding='UTF-8') as test_file:
            test_text = test_file.read()
            assert len(reference_text) == len(test_text)


def test_summary_locus_nbr_probe_with_bcd(setup):
    path_result_folder = setup['lib_by_probe_nbr_bcd_path']
    library = setup['lib_by_probe_nbr_bcd']
    path_output = "resources/design_by_probe_nbr_bcd/OUT"
    summary_test = path_result_folder / "3_Library_summary.csv"
    summary_output_reference = path_output + os.sep + "3_Library_summary.csv"

    with open(summary_test, mode="w", encoding="UTF-8") as file:
        file.write("Chromosome,Locus_N°,Start,End,Region size, Barcode,PU.Fw,PU.Rev,Nbr_Probes\n")
        for locus in library.loci_list:
            file.write(
                f"{locus.chr_name},{locus.locus_n},{locus.start_seq},\
{locus.end_seq},{locus.end_seq - locus.start_seq},{locus.bcd_locus},{locus.primers_univ[0]},\
{locus.primers_univ[2]},{len(locus.seq_probe)}\n"
            )

    with open(summary_output_reference, mode='r', encoding='UTF-8') as reference_file:
        reference_text = reference_file.read()
        with open(summary_test, mode='r', encoding='UTF-8') as test_file:
            test_text = test_file.read()
            assert len(reference_text) == len(test_text)



def test_summary_locus_nbr_probe_with_rt(setup):
    path_result_folder = setup['lib_by_probe_nbr_rt_path']
    library = setup['lib_by_probe_nbr_rt']
    path_output = "resources/design_by_probe_nbr_rt/OUT"
    summary_test = path_result_folder / "3_Library_summary.csv"
    summary_output_reference = path_output + os.sep + "3_Library_summary.csv"

    with open(summary_test, mode="w", encoding="UTF-8") as file:
        file.write("Chromosome,Locus_N°,Start,End,Region size, Barcode,PU.Fw,PU.Rev,Nbr_Probes\n")
        for locus in library.loci_list:
            file.write(
                f"{locus.chr_name},{locus.locus_n},{locus.start_seq},\
{locus.end_seq},{locus.end_seq - locus.start_seq},{locus.bcd_locus},{locus.primers_univ[0]},\
{locus.primers_univ[2]},{len(locus.seq_probe)}\n"
            )

    with open(summary_output_reference, mode='r', encoding='UTF-8') as reference_file:
        reference_text = reference_file.read()
        with open(summary_test, mode='r', encoding='UTF-8') as test_file:
            test_text = test_file.read()
            assert len(reference_text) == len(test_text)