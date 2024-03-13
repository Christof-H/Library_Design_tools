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
import json

import datetime as dt
import modules.data_function as data
from models.library import Library
from models.locus import Locus
from models.invalidNbrLocusException import InvalidNbrLocusException


# ---------------------------------------------------------------------------------------------
#                                       Functions
# ---------------------------------------------------------------------------------------------
def print_dashline():
    """print a dash line"""
    print("-" * 70)


def check_locus_rt_bcd():
    """Check that there are enough barcodes or RTs for the total number of loci.

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


# ---------------------------------------------------------------------------------------------
#                               Importing library parameters
# ---------------------------------------------------------------------------------------------
src_folder = os.path.dirname(os.path.realpath(__file__))
script_folder = os.path.abspath(os.path.join(src_folder, ".."))

PRIMER_UNIV_FILE = "Primer_univ.csv"
JSON_FILE = "input_parameters.json"

# Retrieving parameters from the input_parameters.json file
json_path = src_folder + os.sep + JSON_FILE
parameters = data.load_parameters(json_path)
parameters["resources_path"] = src_folder + os.sep + "resources"
parameters["bcd_rt_path"] = (
    parameters["resources_path"] + os.sep + parameters["bcd_rt_file"]
)
parameters["primer_univ_path"] = (
    parameters["resources_path"] + os.sep + PRIMER_UNIV_FILE
)


# ---------------------------------------------------------------------------------------------
#                                   Creating result folder
# ---------------------------------------------------------------------------------------------
result_folder = script_folder + os.sep + "Library_Design_Results"
if not os.path.exists(result_folder):
    os.mkdir(result_folder)

# ---------------------------------------------------------------------------------------------
#                           Formatting and storage of sequences
#               (primers, TRs, barcodes, genomics) in corresponding variables
# ---------------------------------------------------------------------------------------------

# Opening and formatting barcodes or RTs in the bcd_RT variable:
bcd_rt_list = data.bcd_rt_format(parameters["bcd_rt_path"])

# Opening and formatting the coordinates and genomic sequences of in the list_seq_genomic variable :
list_seq_genomic = data.seq_genomic_format(parameters["genomic_path"])

# Opening and formatting universal primers in the primer_univ variable : :
primer_univ_list = data.universal_primer_format(parameters["primer_univ_path"])

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
check_locus_rt_bcd()

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
library = Library(
    chromosome_name=parameters["chromosome_file"].split(".")[0],
    start_lib=parameters["start_lib"],
    nbr_loci_total=parameters["nbr_loci_total"],
    max_diff_percent=parameters["max_diff_percent"],
    design_type=parameters["design_type"],
)


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
path_result_folder = result_folder + os.sep + date_now
os.mkdir(path_result_folder)

# writing the file with detailed information (information for each locus and sequence)
data.result_details_file(path_result_folder, library)

# writing the file with all primary probe sequences for all locus (without spaces)
data.full_sequences_file(path_result_folder, library)

# writing file with summary information (without sequence) in the form of a table
data.library_summary_file(path_result_folder, library)


# Retrieve the parameters used to design the library
output_parameters = copy.deepcopy(parameters)
output_parameters["Script_Name"] = "library_design.py"
output_parameters["primer_Univ_File"] = PRIMER_UNIV_FILE


# Write library parameters in the 4-OutputParameters.json file
data.save_parameters(path_result_folder, output_parameters)
