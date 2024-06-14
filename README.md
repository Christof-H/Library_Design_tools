## Overview

The purpose of this software is to generate a library consisting of a set of primary probes designed to visualize a locus of interest segmented into several regions, using the multiplexed-FISH (Fluorescence In Situ Hybridization) technique. These primary probes consist of a concatenation of sequences, each with a specific role:

- Primary probes contain a central sequence (30 to 35 bases) complementary to the genomic DNA fragment to be targeted.
- For each region of the locus studied, a specific detection sequence is assigned.  These sequences are repeated within the primary probes to increase the detection threshold (max=5). They are complementary either to imaging oligo sequences for direct labeling, or to bridges for indirect labeling. In this way, each region of the locus is targeted by primary probes with a unique detection sequence.
- Finally, the primary probes are also flanked on either side by sequences enabling amplification of the pool of primary probes making up this library.

#### Explanation of the procedure for the production of primary probes by the script

1. Assigning genomic sequences to loci

The user can choose to design a library according to a specific locus size, or a specific number of probes per locus. 

- If the user has chosen to design a library based on a locus size:

The script will calculate the coordinates of each locus according to the starting coordinates of the 1st locus (`start_lib`), the resolution (`resolution`) and the total number of loci chosen (`nbr_loci_total`).
Then the script will search all the genomic sequences according to each locus coordinate in the `chromosome_file`. If the number of primary probes found is greater than the number of desired primary probes (`nbr_probe_by_locus`), the script will choose (randomly among all sequences) the number of desired primary probes. Conversely, if the number of primary probes found is smaller than the number of desired primary probes (`nbr_probe_by_locus`), the script will leave all primary probes found.

- If the user has chosen to design a library based on a number of probes per locus:

The script will assign genomic sequences sequentially until the number of primary probes selected for each locus has been reached.

2. Completion of primary sequences with barcodes/RT and universal primers 

To the genomic sequences, the script will add the sequences of the barcodes/RT according to each locus.

3. Completion of primary sequences with universal primers 

Finally, the script will add identical sequences to the ends of the primary probes, enabling the oligo pool to be amplified.

4. Verification of the homogeneity of the size of the probes 

If the size of the primary probes varies by more than the `max_diff_percent`, the script will perform a 3' completion with random nucleotides.

5. Writing the different files in a result folder

**1_Library_details.txt**: All primary probe sequences are grouped by locus, with corresponding information (start-end-Bcr/RT). Each primary probe is subdivided into distinct parts in order to separate the different regions (primerU, Bcd/RT, sequence homologous to genomic DNA)  

**2_Full_sequence_Only.txt**: File containing all the sequences of the raw primary probes (without any information). This is the file that is used for ordering the library.  

**3_Library_Summary.csv**: Table summarizing all the information about each locus (locus number, start, end, Bcd/RT, PU.fw, PU.rev, number of probes per locus...)   

**4-OutputParameters.json**: Json file containing all the parameters that have been used to produce the library, in order to have a backup if needed later. 



## Script installation procedure

1. Recovery of genomic DNA sequences

This software is based on the use of pre-designed genomic sequences using an open-source script: OligoMiner (Beliveau & al. PNAS 2018, doi: 10.1073/pnas.1714530115)

Download the genomic DNA sequences supplied by OligoMiner, corresponding to the genome and chromosome of your [choice](https://oligopaints.hms.harvard.edu/genome-files).

2. Checking the tools needed to use the script

To check that Python is installed and the required version (version >=3.10), open a terminal and run:

```bash
$ python3 --version
```

If you encounter an error or the pyhton version is lower than 3.10, install python 3.10:

```bash
$ sudo apt update
$ sudo apt install python3.10 
```

Check if Tkinter, a standard GUI (Graphical User Interface) library for Python, is installed.

```bash
$ python3 -m tkinter
```

If Tkinter is installed correctly, this will open a window displaying the version of Tkinter, otherwise you will encounter an error.

If Tkinter is not installed, run:

```bash
$ sudo apt install python3-tk
```

Check that the pip package manager is installed:

```bash
$ pip --version 
#or
$ pip3 --version
```

If not, install the package manager:

```bash
$ python get-pip.py
```

3. Create a blank environment compatible with the script

In the directory of your choice, create a directory where you will store your blank environment, and access it:

```bash
$ mkdir myEnvFolder && cd myEnvFolder
```

Creating your new environment:

```bash
$ python -m venv myenv
```

Activate your new blank environment:

```bash
$ source myenv/bin/activate
```

You should see (myenv) in front of your command prompt, indicating that the virtual environment is enabled:

```bash
(myenv)$
```

4. Script installation in your activated virtual environment

```bash
(myenv)$ pip install .....
```



## Using the script

You have the option of running the script with a CLI (Command Line Interface) or with a GUI (Graphical User Interface).
If you want to run the script with the CLI, you first need to modify the `inputs_parameters.json` file, which contains the parameters for designing your library.
If you want to run this script with the GUI, you can modify these parameters directly in the interface itself

1. Using CLI

This input_parameters.json file is located in the `src/resources` folder.

**Change the settings for the design of your library, if necessary:**  

- `chromosome_file` (string): Name of the file containing the sequences homologous to the genomic DNA (ex: 'chr2L.bed') 
- `chromosome_folder` (string): Folder where the file containing the sequences homologous to the genomic DNA is located
- `design_type` (string): 'nbr_probes' or 'locus_length. Choose the type of library design, either according to the size of each locus, or according to the number of primary probes per locus. 
- `resolution` (integer): Size for each locus in nucleotides
- `start_lib` (integer): Start genomic coordinate of the 1st locus
- `nbr_loci_total` (integer): Total number of loci
- `nbr_probe_by_locus` (integer): Number of primary probes per locus
- `nbr_bcd_rt_by_probe` (integer): Number of the same barcode per primary probe (max=5)
- `primer_univ` (string): Choice of the pair of universal primers 'primer1', 'primer2' until 'primer8' (ex: 'primer1')
- `bcd_rt_file` (string): Allows you to choose the type of labeling, either direct labeling with imaging oligos (RTs) or indirect labeling using bridges (Barcodes).'List_RT.csv' or 'Barcodes.csv'
- `max_diff_percent` (integer): the permitted difference in size between the smallest and largest primary probe sequences

Once you have modified the parameters, you can run scipt by specifying the CLI arguments.

- **-c, --cli**:    If the option is not specified, the program will launch a graphical user interface
- **-p, --parameters**:    Path of the parameters.json file. DEFAULT: default input_parameters.json file in `src/resources`
- **-o, --output**:     Folder to save results files. DEFAULT: current working directory

2. Using GUI

If you are using the graphical interface, there is no need to modify the `input_parameters.json` file. You can make the changes directly in the GUI.

To launch the graphical interface:

```bash
(myenv)$ ...
```

Using the graphical interface, you can then easily visualize the design of your library:

- in the **Graphic result** tab: you will have a graphical view of the number of probes per locus, or a view of the size of the locus depending on the type of design chosen
- in the **Library details** tab: a summary in table form of the main information concerning the design of your library.



