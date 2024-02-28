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
Library_Summary.csv file containing a table summarising all the information on each 
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
import random
import copy
import json


import datetime as dt
import modules.data_import_fonction as data
from models.Library import *
from models.Locus import *

# ---------------------------------------------------------------------------------------------
#                               Importing library parameters
# ---------------------------------------------------------------------------------------------
rootFolder = os.getcwd()


JSON_FILE = "input_parameters.json"
PRIMER_UNIV_FILE = "Primer_univ.csv"

jsonPath = rootFolder + os.sep + "src" + os.sep + JSON_FILE
with open(jsonPath, mode="r", encoding="UTF-8") as file:
    input_parameters = json.load(file)


chromosomeFile = input_parameters["ChromosomeFile"]
chromosomeFolder = input_parameters["ChromosomeFolder"]
resolution = input_parameters["resolution"]
startLib = input_parameters["startLib"]
nbrLociTotal = input_parameters["nbrLociTotal"]
nbrProbeByLocus = input_parameters["nbrProbeByLocus"]
nbrBcd_RT_ByProbe = input_parameters["nbrBcd_RT_ByProbe"]
PrimerU = input_parameters["PrimerU"]
bcd_RT_File = input_parameters["bcd_RT_File"]
max_diff_pourcent = input_parameters["max_diff_pourcent"]
endLib = startLib + (nbrLociTotal * resolution)




resources_path = rootFolder + os.sep + "resources"
bcd_RT_Path = resources_path + os.sep + bcd_RT_File
genomic_Path = chromosomeFolder + os.sep + chromosomeFile
primer_Univ_Path = rootFolder + os.sep + PRIMER_UNIV_FILE

# ---------------------------------------------------------------------------------------------
#                                   Creating result folder
# ---------------------------------------------------------------------------------------------
resultFolder = rootFolder + os.sep + "Library_Design_Results"
if not os.path.exists(resultFolder):
    os.mkdir(resultFolder)

# ---------------------------------------------------------------------------------------------
#                           Formatting and storage of sequences
#               (primers, TRs, barcodes, genomics) in corresponding variables
# ---------------------------------------------------------------------------------------------

# Opening and formatting barcodes or RTs in the bcd_RT variable:
bcd_RT = data.bcd_RT_format(bcd_RT_Path)

# Opening and formatting the coordinates and genomic sequences of in the listSeqGenomic variable :
listSeqGenomic = data.seq_genomic_format(genomic_Path)

# Opening and formatting universal primers in the primerUniv variable : :
primerUniv = data.universal_Primer_format(primer_Univ_Path)


print("-" * 70)
print("listSeqGenomic =", listSeqGenomic[0])
print("-" * 70)
print("bcd_RT =", bcd_RT[:2])
print("-" * 70)
print("primerUniv = ", "primer1 =", primerUniv["primer1"])
print("-" * 70)

# ---------------------------------------------------------------------------------------------
#                               Filling locus information 
#           (Primers Univ, start coordinates, end coordinates, DNA genomic sequences)
# ---------------------------------------------------------------------------------------------

# Search for the desired universal primers
primer = [primerUniv[x] for x in primerUniv.keys() if x == PrimerU]
primer = primer[0]

# Calculation of start and end coordinates for each locus
startPositions = [startLib + x * resolution for x in range(nbrLociTotal)]
endPositions = [startLib + (x + 1) * resolution for x in range(nbrLociTotal)]

# Filling the Library class with all the Locus
library = Library()
for i, start, end in zip(range(nbrLociTotal), startPositions, endPositions):
    library.add_locus(
        Locus(
            locus_n=i + 1,
            chr_name=chromosomeFile.split(".")[0],
            start_seq=start,
            end_seq=end,
            primers_univ=primer,
        )
    )


# Allocation of the genomic DNA sequences of the primary probes for each locus of the Library according to the coordinates (start, end)
for locus in library.total_loci:
    temp = []
    for seq in listSeqGenomic:
        if locus.start_seq <= int(seq[0]) and int(seq[1]) < locus.end_seq:
            temp.append([seq[0], seq[2]])
        else:
            pass

    if len(temp) > nbrProbeByLocus:
        random.shuffle(temp)
        temp = temp[:nbrProbeByLocus]
        temp.sort()
    locus.seq_probe = [x[1] for x in temp]

# Display of a locus as an example
print('-'*70)
print ("Locus exemple :")
print(library.total_loci[0])


# Sequences for barcodes/RTs added to primary probes according to locus
count = 0
for locus in library.total_loci:
    seqWithBcd = []
    bcd_RT_seq = bcd_RT[count][1]

    for genomic_seq in locus.seq_probe:
        if nbrBcd_RT_ByProbe == 2:
            seqWithBcd.append(f"{bcd_RT_seq} {genomic_seq} {bcd_RT_seq}")
        elif nbrBcd_RT_ByProbe == 3:
            seqWithBcd.append(f"{bcd_RT_seq} {genomic_seq} {bcd_RT_seq * 2}")
        elif nbrBcd_RT_ByProbe == 4:
            seqWithBcd.append(f"{bcd_RT_seq * 2} {genomic_seq} {bcd_RT_seq * 2}")
        elif nbrBcd_RT_ByProbe == 5:
            seqWithBcd.append(f"{bcd_RT_seq * 3} {genomic_seq} {bcd_RT_seq * 2}")
    count += 1
    locus.seq_probe = seqWithBcd


# Sequences for universal primers added to the primary probes at each end

for locus in library.total_loci:
    pFw = copy.deepcopy(locus.primers_univ[1])
    pRev = copy.deepcopy(locus.primers_univ[3])
    temp = list()
    temp = [f"{pFw} {x} {pRev}" for x in locus.seq_probe]
    # temp=[pFw+' '+ x +' '+pRev for x in locus.seqProbe]
    locus.seq_probe = temp

# Display example of a final primary probe sequence
print("-" * 70)
print("example of a primary probe sequence :")
print("-" * 70)
print(library.total_loci[0].seq_probe[0])

# ---------------------------------------------------------------------------------------------
#                               Checking and completion
# ---------------------------------------------------------------------------------------------

# Checking primary probes length for all Locus
min_length, max_length, diff_nbr, diff_pourcentage = library.check_length_seq_diff()
print('-'*70)
print(f"minimum size for all probes combined : {min_length}")
print(f"maximum size for all probes combined : {max_length}")
print(f"difference in size : {diff_pourcentage:.1f}%")

# If there is a significant difference in size between the primary probes of all the Locus,
#completion primary probes too small to standardise the length of the oligo-pool
# ATTENTION: 3' completion of the sequence
library.completion(diff_pourcentage, max_length, max_diff_pourcent)


# ---------------------------------------------------------------------------------------------
#                           Writing the various results files
# ---------------------------------------------------------------------------------------------

# Creation of a dated file to differentiate between the different libraries designed
date_now = dt.datetime.now().strftime("%Y%m%d_%H%M")
pathResultFolder = resultFolder + os.sep + date_now
os.mkdir(pathResultFolder)


# writing the file with detailed information (information for each locus and sequence)
resultDetails = pathResultFolder + os.sep + "1_Library_details.txt"
with open(resultDetails, mode="w", encoding="UTF-8") as file:
    for locus in library.total_loci:
        file.write(
            f"Chromosome: {locus.chr_name} Locus_N°{locus.locus_n}\
 Start:{locus.start_seq} End:{locus.end_seq} Bcd_locus:{locus.bcd_locus}\n"
        )
        for seq in locus.seq_probe:
            file.write(seq + "\n")

# writing the file with all primary probe sequences for all locus (without spaces)
fullSequence = pathResultFolder + os.sep + "2_Full_sequence_Only.txt"
with open(fullSequence, mode="w", encoding="UTF-8") as file:
    for locus in library.total_loci:
        for seq in locus.seq_probe:
            file.write(seq.replace(" ", "") + "\n")

# writing file with summary information (without sequence) in the form of a table
Summary = pathResultFolder + os.sep + "3_Library_Summary.csv"
with open(Summary, mode="w", encoding="UTF-8") as file:
    file.write("Chromosome,Locus_N°,Start,End,Barcode,PU.Fw,PU.Rev,Nbr_Probes\n")
    for locus in library.total_loci:
        file.write(
            f"{locus.chr_name},{locus.locus_n},{locus.start_seq},\
{locus.end_seq},{locus.bcd_locus},{locus.primers_univ[0]},\
{locus.primers_univ[2]},{len(locus.seq_probe)}\n"
        )

# Saving the parameters used to generate the library as a .json file

parametersFilePath = pathResultFolder + os.sep + "4-OutputParameters.json"

# Parameter recovery
parameters = {}
parameters["Script_Name"] = "library_design.py"
parameters["ChromosomeFile"] = chromosomeFile
parameters["ChromosomeFolder"] = chromosomeFolder
parameters["resolution"] = resolution
parameters["startLib"] = startLib
parameters["endLib"] = startLib + (resolution * nbrLociTotal)
parameters["nbrLociTotal"] = nbrLociTotal
parameters["nbrProbeByLocus"] = nbrProbeByLocus
parameters["nbrBcd_RT_ByProbe"] = nbrBcd_RT_ByProbe
parameters["PrimerU"] = PrimerU
parameters["bcd_TR_File"] = bcd_RT_File
parameters["primer_Univ_File"] = PRIMER_UNIV_FILE


# Write the 4-OutputParameters.json file
with open(parametersFilePath, mode="w", encoding="UTF-8") as file:
    json.dump(parameters, file, indent=4)


print(f"All files concerning your library design are saved in {pathResultFolder}/")
