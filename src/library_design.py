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
import modules.data_import_function as data
from models.library import Library
from models.locus import Locus
from models.invalidNbrLocusException import InvalidNbrLocusException

# ---------------------------------------------------------------------------------------------
#                               Importing library parameters
# ---------------------------------------------------------------------------------------------
src_folder = os.path.dirname(os.path.realpath(__file__))
script_folder = os.path.abspath(os.path.join(src_folder, ".."))

JSON_FILE = "input_parameters.json"
PRIMER_UNIV_FILE = "Primer_univ.csv"

json_path = src_folder + os.sep + JSON_FILE
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

resources_path = src_folder + os.sep + "resources"
bcd_rt_path = resources_path + os.sep + bcd_rt_file
genomic_path = chromosome_folder + os.sep + chromosome_file
primer_univ_path = resources_path + os.sep + PRIMER_UNIV_FILE


def print_dashline():
    """print a dashline"""

    print('-' * 70)


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
bcd_RT_list = data.bcd_rt_format(bcd_rt_path)

# Opening and formatting the coordinates and genomic sequences of in the list_seq_genomic variable :
list_seq_genomic = data.seq_genomic_format(genomic_path)

# Opening and formatting universal primers in the primer_univ variable : :
primer_univ_list = data.universal_primer_format(primer_univ_path)

print_dashline()
print("list_seq_genomic =", list_seq_genomic[0])
print_dashline()
print("bcd_RT =", bcd_RT_list[:2])
print_dashline()
print("primer_univ = ", "primer1 =", primer_univ_list["primer1"])
print_dashline()


# ---------------------------------------------------------------------------------------------
#       Check the number of loci against the number of RTs or barcodes available
# ---------------------------------------------------------------------------------------------
def check_locus_rt_bcd():
    """Check that there are enough barcodes or RTs for the total number of loci.

    Raises:
        InvalidNbrLocusException: If the number of available barcodes or RTs is insufficient
            compared to the total number of loci.
    """
    type_bcdrt = "barcodes" if bcd_rt_file == "Barcodes.csv" else "RTs"
    if len(bcd_RT_list) < nbr_loci_total:
        raise InvalidNbrLocusException(nbr_locus=nbr_loci_total, nbr_bcd_rt=len(bcd_RT_list),
                                       type_bcd_rt=type_bcdrt)


check_locus_rt_bcd()

# ---------------------------------------------------------------------------------------------
#                               Filling locus information
#           (Primers Univ, start coordinates, end coordinates, DNA genomic sequences)
# ---------------------------------------------------------------------------------------------

# Search for the desired universal primers
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

# Display of a locus as an example
print_dashline()
print("Locus exemple :")
print(library.loci_list[0])

# Sequences for barcodes/RTs added to primary probes according to locus
count = 0
for locus in library.loci_list:
    seq_with_bcd = []
    bcd_RT_seq = bcd_RT_list[count][1]
    locus.bcd_locus = bcd_RT_list[count][0]

    for genomic_seq in locus.seq_probe:
        if nbr_bcd_rt_by_probe == 2:
            seq_with_bcd.append(f"{bcd_RT_seq} {genomic_seq} {bcd_RT_seq}")
        elif nbr_bcd_rt_by_probe == 3:
            seq_with_bcd.append(f"{bcd_RT_seq} {genomic_seq} {bcd_RT_seq * 2}")
        elif nbr_bcd_rt_by_probe == 4:
            seq_with_bcd.append(f"{bcd_RT_seq * 2} {genomic_seq} {bcd_RT_seq * 2}")
        elif nbr_bcd_rt_by_probe == 5:
            seq_with_bcd.append(f"{bcd_RT_seq * 3} {genomic_seq} {bcd_RT_seq * 2}")
    count += 1
    locus.seq_probe = seq_with_bcd

# Sequences for universal primers added to the primary probes at each end

for locus in library.loci_list:
    p_fw = copy.deepcopy(locus.primers_univ[1])
    p_rev = copy.deepcopy(locus.primers_univ[3])
    temp = list()
    temp = [f"{p_fw} {x} {p_rev}" for x in locus.seq_probe]
    locus.seq_probe = temp

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
pathresult_folder = result_folder + os.sep + date_now
os.mkdir(pathresult_folder)

# writing the file with detailed information (information for each locus and sequence)
result_details = pathresult_folder + os.sep + "1_Library_details.txt"
with open(result_details, mode="w", encoding="UTF-8") as file:
    for locus in library.loci_list:
        file.write(
            f"Chromosome: {locus.chr_name} Locus_N°{locus.locus_n}\
 Start:{locus.start_seq} End:{locus.end_seq} Bcd_locus:{locus.bcd_locus}\n"
        )
        for seq in locus.seq_probe:
            file.write(seq + "\n")

# writing the file with all primary probe sequences for all locus (without spaces)
full_sequence = pathresult_folder + os.sep + "2_Full_sequence_Only.txt"
with open(full_sequence, mode="w", encoding="UTF-8") as file:
    for locus in library.loci_list:
        for seq in locus.seq_probe:
            file.write(seq.replace(" ", "") + "\n")

# writing file with summary information (without sequence) in the form of a table
summary = pathresult_folder + os.sep + "3_Library_summary.csv"
with open(summary, mode="w", encoding="UTF-8") as file:
    file.write("Chromosome,Locus_N°,Start,End,Region size, Barcode,PU.Fw,PU.Rev,Nbr_Probes\n")
    for locus in library.loci_list:
        file.write(
            f"{locus.chr_name},{locus.locus_n},{locus.start_seq},\
{locus.end_seq},{locus.end_seq - locus.start_seq},{locus.bcd_locus},{locus.primers_univ[0]},\
{locus.primers_univ[2]},{len(locus.seq_probe)}\n"
        )

# Saving the parameters used to generate the library as a .json file

parameters_file_path = pathresult_folder + os.sep + "4-OutputParameters.json"

# Parameter recovery
parameters = {}
parameters["Script_Name"] = "library_design.py"
parameters["chromosome_file"] = chromosome_file
parameters["chromosome_folder"] = chromosome_folder
parameters["resolution"] = resolution
parameters["start_lib"] = start_lib
parameters["end_lib"] = start_lib + (resolution * nbr_loci_total)
parameters["nbr_loci_total"] = nbr_loci_total
parameters["nbr_probe_by_locus"] = nbr_probe_by_locus
parameters["nbr_bcd_rt_by_probe"] = nbr_bcd_rt_by_probe
parameters["primer_univ"] = primer_univ
parameters["bcd_TR_File"] = bcd_rt_file
parameters["primer_Univ_File"] = PRIMER_UNIV_FILE
parameters["max_diff_percent"] = max_diff_percent
parameters["design_type"] = design_type

# Write the 4-OutputParameters.json file
with open(parameters_file_path, mode="w", encoding="UTF-8") as file:
    json.dump(parameters, file, indent=4)

print(f"All files concerning your library design are saved in {pathresult_folder}/")
