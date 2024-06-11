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
     iiii) check the homogeneity of the size of the different probes.
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
from pathlib import Path

from core.args import parse_arguments, check_args
from core.design_process import design_process
from core.app_gui import main_gui


def main():
    """Main function of library design script"""

    # ---------------------------------------------------------------------------------------------
    #                                   CLI Arguments
    # ---------------------------------------------------------------------------------------------

    args = parse_arguments()
    check_args(args)
    print(args)

    if not args.cli:
        json_parameters_path = args.parameters
        output_folder = args.output
        design_process(output_folder=output_folder, json_path=json_parameters_path)
    else:
        main_gui()


if __name__ == "__main__":
    main()
