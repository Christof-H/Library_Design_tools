import json
from json import JSONDecodeError
from pathlib import Path

from models.library import Library


def load_parameters(json_path: Path) -> dict[str, str | int | Path]:
    """Load parameters from parameter json file

    Args:
        json_path (Path):
            File path of parameter json file

    Returns:
        dict[str, str | int | Path]: dictionary containing parameters for library design
    """
    primer_univ_file = "Primer_univ.csv"
    src_folder = Path(__file__).absolute().parents[1]

    with open(json_path, mode="r", encoding="UTF-8") as file:
        try:
            input_param = json.load(file)
        except JSONDecodeError:
            print("The parameter file is not a Json file")

        input_param["end_lib"] = input_param["start_lib"] + (
            input_param["nbr_loci_total"] * input_param["resolution"]
        )
        input_param["resources_path"] = src_folder.joinpath("resources")

        #Adds a default path for the chromosome folder when this is not specified in input_parameters.json
        #(when using the script for a test)
        if input_param["chromosome_folder"]:
            input_param["chromosome_folder"] = Path(input_param["chromosome_folder"])
            input_param["genomic_path"] = input_param["chromosome_folder"].joinpath(
                input_param["chromosome_file"])
        else:
            input_param["chromosome_folder"] = input_param["resources_path"]
            input_param["genomic_path"] = input_param["chromosome_folder"].joinpath(
                input_param["chromosome_file"])

        input_param["bcd_rt_path"] = input_param["resources_path"].joinpath(
            input_param["bcd_rt_file"]
        )
        input_param["primer_univ_file"] = primer_univ_file
        input_param["primer_univ_path"] = input_param["resources_path"].joinpath(
            input_param["primer_univ_file"]
        )
        return input_param


def universal_primer_format(path: Path) -> dict[str, list[str]]:
    """Function for opening, formatting and storing universal primer sequences.

    Args:
        path (Path): File path of universal primer couple

    Returns:
        dict[str, list[str]]: name and sequence for universal primer
    """
    primer_univ = {}
    with open(path, mode="r", encoding="utf-8") as file:
        for line in file:
            data = line.replace("\n", "").split(",")
            primer_univ[data[0]] = [item for item in data[1:]]
    return primer_univ


def bcd_rt_format(path: Path) -> list[list[str]]:
    """Function for opening, formatting and storing barcode or RT sequences.

    Args:
        path (Path): File path of Barcodes or RT

    Returns:
        list[list[str]]: a list of barcode or RT [[name, sequence], ...]
    """

    bcd_rt_list = []
    with open(path, mode="r", encoding="utf-8") as file:
        for line in file:
            data = line.replace("\n", "").split(",")
            bcd_rt_list.append(data)
        return bcd_rt_list


def seq_genomic_format(path: Path) -> list[int, int, str]:
    """Function for opening, formatting and storing genomic sequences.

    Args:
        path (Path): File path of genomic sequences

    Returns:
        list[int, int, str]: sequence of genomic DNA with coordinates
    """
    seq_genomic_list = []
    with open(path, mode="r", encoding="UTF-8") as file:
        for line in file:
            data = line.split("\t")
            seq_genomic_list.append([int(data[1]), int(data[2]), data[3]])
    return seq_genomic_list


def result_details_file(path_result_folder: Path, library: Library) -> None:
    """Saves separate sequences for each locus (with the corresponding locus information).

    Args:
        path_result_folder (Path):
            Folder path for results files
        library (Library):
            library containing all information and sequences
    """
    result_details = path_result_folder.joinpath("1_Library_details.txt")
    with open(result_details, mode="w", encoding="UTF-8") as file:
        for locus in library.loci_list:
            file.write(
                f"Chromosome: {locus.chr_name} Locus_N°{locus.locus_n}\
Start:{locus.start_seq} End:{locus.end_seq} Bcd_locus:{locus.bcd_locus}\n"
            )
            for seq in locus.seq_probe:
                file.write(seq + "\n")


def full_sequences_file(path_result_folder: Path, library: Library) -> None:
    """Save all the sequences in the library without any information.

    Args:
        path_result_folder (Path):
            Folder path for results files
        library (Library):
            library containing all information and sequences
    """
    full_sequence = path_result_folder.joinpath("2_Full_sequence_Only.txt")
    with open(full_sequence, mode="w", encoding="UTF-8") as file:
        for locus in library.loci_list:
            for seq in locus.seq_probe:
                file.write(seq.replace(" ", "") + "\n")


def library_summary_file(path_result_folder: Path, library: Library) -> None:
    """Save a csv file with a summary of the various information concerning the loci in the
    library (locus number, start, end, region size, universal primer...).

    Args:
        path_result_folder (Path):
            Folder path for results files
        library (Library):
            library containing all information and sequences
    """

    summary = path_result_folder.joinpath("3_Library_summary.csv")
    with open(summary, mode="w", encoding="UTF-8") as file:
        file.write(
            "Chromosome,Locus_N°,Start,End,Region size, Barcode,PU.Fw,PU.Rev,Nbr_Probes\n"
        )
        for locus in library.loci_list:
            file.write(
                f"{locus.chr_name},{locus.locus_n},{locus.start_seq},\
{locus.end_seq},{locus.end_seq - locus.start_seq},{locus.bcd_locus},{locus.primers_univ[0]},\
{locus.primers_univ[2]},{len(locus.seq_probe)}\n"
            )


def save_parameters(
    path_result_folder: Path, out_parameters: dict[str, str | int | Path]
) -> None:
    """Save all parameters used to design librairy in a json file.

    Args:
        path_result_folder (Path):
            Folder path for results files
        out_parameters (dict):
            dictionary with specific parameters
    """
    parameters_file_path = path_result_folder.joinpath("4-OutputParameters.json")
    # Convert all Path  object in str (Object of type PosixPath is not JSON serializable)
    out_parameters["genomic_path"] = out_parameters["genomic_path"].as_posix()
    out_parameters["resources_path"] = out_parameters["resources_path"].as_posix()
    out_parameters["bcd_rt_path"] = out_parameters["bcd_rt_path"].as_posix()
    out_parameters["primer_univ_path"] = out_parameters["primer_univ_path"].as_posix()
    out_parameters["output_folder"] = out_parameters["output_folder"].as_posix()
    out_parameters["path_result_folder"] = out_parameters[
        "path_result_folder"
    ].as_posix()
    out_parameters["chromosome_folder"] = out_parameters["chromosome_folder"].as_posix()

    path_str = path_result_folder.as_posix()
    with open(parameters_file_path, mode="w", encoding="UTF-8") as file:
        json.dump(out_parameters, file, indent=4)

    print(f"All files concerning your library design are saved in {path_str}/")


def recover_summary(summary_path: Path) -> tuple[list[str], list[list[str]]]:
    with open(file=summary_path, mode="r", encoding="utf-8") as sum_file:
        i = 1
        values = []
        for line in sum_file:
            if i == 1:
                columns = [x for x in line.replace("\n", "").split(",")]
                i += 1
            else:
                values.append([x for x in line.replace("\n", "").split(",")])
        return columns, values


def recover_info_text(info_json: Path) -> dict[str:str]:
    with open(file=info_json, mode="r", encoding="UTF-8") as file:
        data = json.load(file)
    return data
