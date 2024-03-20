#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 16:07:15 2021

@author: Christophe Houbron

This script is used to design the primary probes corresponding to the genomic regions to be studied.
Each primary probe contains a number (2 to 5) of a readout sequence specific to each locus, 
a sequence (30-35 bases) complementary to the genomic DNA, and sequences on either side of 
the oligo to allow amplification of the library.  

Using the parameters, the script will :
     i) calculate the coordinates for each locus 
     ii) select primary probe sequences for each locus 
     iii) concatenate primary sequences with readout sequence and universal primers
     iiii) check the homogeneity of the size of the differents probes. 
Several output text files are created after running the Library_Design.py script. 
Library_summary.csv file containing a table summarising all the information on each 
locus (locus number, start position, end position, readout probe, primer forward, primer reverse, 
number of probes per locus). 
A Json file (outputParameters.json) containing all the parameters used to generate the library, 
in order to have a backup if needed later. 
And a file called Full_sequence_Only.txt containing all the raw primary probe sequences of oligos 
used to order the microarray from an oligopool synthesizer company.
It is possible to embed multiple libraries within one oligopool by using different sets of 
universal primers.

"""
import os
import copy
from pathlib import Path

import datetime as dt
from argparse import ArgumentParser

import modules.data_function as df
from models.library import Library
from models.locus import Locus
from models.invalidNbrLocusException import InvalidNbrLocusException


# ---------------------------------------------------------------------------------------------
#                                       Functions
# ---------------------------------------------------------------------------------------------
def print_dashline():
    """print a dash line"""
    print("-" * 70)


def check_locus_rt_bcd(
    parameters: dict[str, str | int], bcd_rt_list: list[list[str]]
) -> None:
    """Check that there are enough barcodes or RTs for the total number of loci.
    Args:
        parameters (dict[str, str | int]):
            parameters in a dictionary
        bcd_rt_list (list[list[str]]):
            a list of barcodes or RT in format [name, sequence]

    Raises:
        InvalidNbrLocusException: If the number of available barcodes or RTs is insufficient
            compared to the total number of loci.
    """
    type_bcdrt = "barcodes" if parameters["bcd_rt_file"] == "Barcodes.csv" else "RTs"
    if len(bcd_rt_list) < parameters["nbr_loci_total"]:
        raise InvalidNbrLocusException(
            nbr_locus=parameters["nbr_loci_total"],
            nbr_bcd_rt=len(bcd_rt_list),
            type_bcd_rt=type_bcdrt,
        )


def main():
    """Main function of library design script"""
    primer_univ_file = "Primer_univ.csv"
    json_file = "input_parameters.json"
    src_folder = Path(__file__).absolute().parent
    script_folder = src_folder.parent

    # ---------------------------------------------------------------------------------------------
    #                                   CLI Arguments
    # ---------------------------------------------------------------------------------------------
    parser = ArgumentParser()

    parser.add_argument(
        "-p",
        "--parameters",
        type=str,
        default=src_folder.joinpath("resources", json_file),
        help="Path of the parameters.json folder.\nDEFAULT: folder containing a default input_parameters.json file",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=script_folder.joinpath("Library_Design_Results"),
        help="Path folder to save results files.\nDEFAULT: folder script",
    )
    args = parser.parse_args()

    # ---------------------------------------------------------------------------------------------
    #                               Importing library parameters
    # ---------------------------------------------------------------------------------------------

    # Retrieving parameters from the input_parameters.json file
    # json_path = args.parameters
    # TODO: choisir entre args.parameters ou json_path = args.parameters
    parameters = df.load_parameters(args.parameters)
    parameters["resources_path"] = src_folder.joinpath("resources")
    parameters["bcd_rt_path"] = parameters["resources_path"].joinpath(
        parameters["bcd_rt_file"]
    )
    parameters["primer_univ_path"] = parameters["resources_path"].joinpath(
        primer_univ_file
    )

    # ---------------------------------------------------------------------------------------------
    #                                   Creating result folder
    # ---------------------------------------------------------------------------------------------
    # TODO: choisir entre args.output ou result_folder = args.output
    # TODO: Quel moyen pour vérifier qu'un argument est la valeur par défaut ou une valeur entrée par l'utilisateur
    # TODO: Faire une fonction dans data_function ???
    if args.output != parser.get_default("output"):
        args.output = Path(args.output).joinpath("Library_Design_Results")
    if not args.output.exists():
        args.output.mkdir()

    # ---------------------------------------------------------------------------------------------
    #                           Formatting and storage of sequences
    #               (primers, TRs, barcodes, genomics) in corresponding variables
    # ---------------------------------------------------------------------------------------------

    # Opening and formatting barcodes or RTs in the bcd_RT variable:
    bcd_rt_list = df.bcd_rt_format(parameters["bcd_rt_path"])

    # Opening and formatting the coordinates and genomic sequences of in the list_seq_genomic variable :
    list_seq_genomic = df.seq_genomic_format(parameters["genomic_path"])

    # Opening and formatting universal primers in the primer_univ variable : :
    primer_univ_list = df.universal_primer_format(parameters["primer_univ_path"])

    print_dashline()
    print("list_seq_genomic =", list_seq_genomic[0])
    print_dashline()
    print("bcd_RT =", bcd_rt_list[:2])
    print_dashline()
    print("primer_univ = ", "primer1 =", primer_univ_list["primer1"])
    print_dashline()

    # ---------------------------------------------------------------------------------------------
    #       Check the number of loci against the number of RTs or barcodes available
    # ---------------------------------------------------------------------------------------------
    check_locus_rt_bcd(parameters, bcd_rt_list)

    # ---------------------------------------------------------------------------------------------
    #                               Filling locus information
    #           (Primers Univ, start coordinates, end coordinates, DNA genomic sequences)
    # ---------------------------------------------------------------------------------------------

    # Search for the desired universal primers
    primer = [
        primer_univ_list[key]
        for key, values in primer_univ_list.items()
        if key == parameters["primer_univ"]
    ]
    primer = primer[0]

    # Create and fill Library object with the different parameters
    library = Library(parameters)

    # Reduce genomic sequence according to loci coordinates or probe number
    list_seq_genomic_reduced = library.reduce_list_seq(
        list_seq_genomic,
        resolution=parameters["resolution"],
        nbr_probe_by_locus=parameters["nbr_probe_by_locus"],
    )

    # Fill the Library object with all the Locus
    for i in range(1, library.nbr_loci_total + 1):
        locus = Locus(
            primers_univ=primer,
            locus_n=i,
            chr_name=library.chromosome_name,
            resolution=parameters["resolution"],
            nbr_probe_by_locus=parameters["nbr_probe_by_locus"],
            design_type=parameters["design_type"],
        )
        list_seq, start, end = locus.recover_genomic_seq(
            i,
            parameters["nbr_loci_total"],
            parameters["start_lib"],
            list_seq_genomic_reduced,
        )
        locus.start_seq = start
        locus.end_seq = end
        # locus.primers_univ=primer,
        locus.seq_probe = list_seq
        library.add_locus(locus)

    # Display of a locus as an example
    print_dashline()
    print("Locus exemple :")
    print(library.loci_list[0])

    # Sequences for barcodes/RTs added to primary probes according to locus
    library.add_rt_bcd_to_primary_seq(bcd_rt_list, parameters)

    # Sequences for universal primers added to the primary probes at each end
    library.add_univ_primer_each_side()

    # Display example of a final primary probe sequence
    print_dashline()
    print("example of a primary probe sequence :")
    print_dashline()
    print(library.loci_list[0].seq_probe[0])

    # ---------------------------------------------------------------------------------------------
    #                               Checking and completion
    # ---------------------------------------------------------------------------------------------

    # Checking primary probes length for all Locus
    min_length, max_length, diff_nbr, diff_percentage = library.check_length_seq_diff()
    print_dashline()
    print("Result of probes checking :")
    print(f"minimum size for all probes combined : {min_length}")
    print(f"maximum size for all probes combined : {max_length}")
    print(f"difference in size : {diff_percentage:.1f}%")

    # If there is a significant difference in size between the primary probes of all the Locus,
    # completion primary probes too small to standardise the length of the oligo-pool
    # ATTENTION: 3' completion of the sequence
    library.completion(diff_percentage, max_length)

    # ---------------------------------------------------------------------------------------------
    #                           Writing the various results files
    # ---------------------------------------------------------------------------------------------

    # Creation of a dated file to differentiate between the different libraries designed
    date_now = dt.datetime.now().strftime("%Y%m%d_%H%M")
    path_result_folder = args.output.joinpath(date_now)
    path_result_folder.mkdir()

    # writing the file with detailed information (information for each locus and sequence)
    df.result_details_file(path_result_folder, library)

    # writing the file with all primary probe sequences for all locus (without spaces)
    df.full_sequences_file(path_result_folder, library)

    # writing file with summary information (without sequence) in the form of a table
    df.library_summary_file(path_result_folder, library)

    # Retrieve the parameters used to design the library
    output_parameters = copy.deepcopy(parameters)
    output_parameters["Script_Name"] = "library_design.py"
    output_parameters["primer_Univ_File"] = primer_univ_file

    # Write library parameters in the 4-OutputParameters.json file
    df.save_parameters(path_result_folder, output_parameters)


if __name__ == "__main__":
    main()
