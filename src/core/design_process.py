import copy
import datetime as dt
from pathlib import Path

import core.data_function as df
from core.function import print_sample, print_dashline, graph_locus_info
from models.locus import check_locus_rt_bcd
from models.locus import Locus
from models.library import Library


def design_process(
    output_folder: Path, json_path: Path = None, inputs_parameters=None
) -> None:
    """All process to design a librairy from parameters

    Args:
        output_folder (Path):
            output folder path to store results files
        json_path (Path):
            input_parameters.json path
        inputs_parameters(dict[str, str | int | Path]):
            dictionary containing parameters

    """
    src_folder_path = Path(__file__).absolute().parents[1]
    # Retrieving parameters from the input_parameters.json file as parameters dictionary
    if json_path:
        parameters = df.load_parameters(json_path)
    else:
        parameters = inputs_parameters

    # ---------------------------------------------------------------------------------------------
    #                                   Creating result folder
    # ---------------------------------------------------------------------------------------------
    result_folder = output_folder.joinpath("Library_Design_Results")
    parameters["output_folder"] = result_folder
    if not result_folder.exists():
        result_folder.mkdir()

    # ---------------------------------------------------------------------------------------------
    #                           Formatting and storage of sequences
    #               (primers, TRs, barcodes, genomics) in corresponding variables
    # ---------------------------------------------------------------------------------------------

    # Opening and formatting barcodes or RTs in the bcd_RT variable:
    bcd_rt_list = df.bcd_rt_format(parameters["bcd_rt_path"])

    # Opening and formatting the coordinates and genomic sequences of in the list_seq_genomic variable :
    list_seq_genomic = df.seq_genomic_format(parameters["genomic_path"])

    # Opening and formatting universal primers in the primer_univ variable :
    primer_univ_list = df.universal_primer_format(parameters["primer_univ_path"])

    print_sample(list_seq_genomic, bcd_rt_list, primer_univ_list)

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
    #                           Create result folder
    # ---------------------------------------------------------------------------------------------

    # Creation of a dated file to differentiate between the different libraries designed
    date_now = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    path_result_folder = result_folder.joinpath(date_now)
    path_result_folder.mkdir()
    parameters["path_result_folder"] = path_result_folder

    # ---------------------------------------------------------------------------------------------
    #                           Display probes/length by locus
    # ---------------------------------------------------------------------------------------------
    list_info = library.recover_loci_probes_length_info()
    graph_locus_info(
        list_info,
        path_result_folder,
        parameters["design_type"],
        parameters["resolution"],
        parameters["nbr_probe_by_locus"],
    )

    # ---------------------------------------------------------------------------------------------
    #                           Writing the various results files
    # ---------------------------------------------------------------------------------------------

    # writing the file with detailed information (information for each locus and sequence)
    df.result_details_file(path_result_folder, library)

    # writing the file with all primary probe sequences for all locus (without spaces)
    df.full_sequences_file(path_result_folder, library)

    # writing file with summary information (without sequence) in the form of a table
    df.library_summary_file(path_result_folder, library)

    # Retrieve the parameters used to design the library
    output_parameters = copy.deepcopy(parameters)
    output_parameters["Script_Name"] = "library_design.py"

    # Write library parameters in the 4-OutputParameters.json file
    df.save_parameters(path_result_folder, output_parameters)
