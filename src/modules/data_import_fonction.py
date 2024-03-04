def universal_primer_format(path : str) -> dict[str, str]:
    """Function for opening, formatting and storing universal primer sequences.

    Args:
        path (str): File path of universal primer couple

    Returns:
        dict[str, list(str)]: name and sequence for universal primer
    """

    primer_univ={}
    with open(path, mode="r", encoding="utf-8") as file:
        for line in file:
            data = line.replace('\n','').split(',')
            primer_univ[data[0]] = [item for item in data[1:]]
    return primer_univ


def bcd_rt_format(path : str) -> list[str]:
    """Function for opening, formatting and storing barcode or RT sequences.

    Args:
        path (str): File path of Barcodes or RT

    Returns:
        list[list[str]]: [[name, sequence], ...]
    """

    bcd_rt_list = []
    with open(path, mode='r', encoding='utf-8') as file:
        for line in file:
            data = line.replace('\n', '').split(',')
            bcd_rt_list.append(data)
        return bcd_rt_list


def seq_genomic_format(path : str) -> list[int , int, str]:
    """Function for opening, formatting and storing genomic sequences.

    Args:
        path (str): File path of genomic sequences

    Returns:
        list[int, int, str]: sequence of genomic DNA with coordinates
    """

    seq_genomic_list = []
    with open(path, mode='r', encoding='UTF-8') as file :
        for line in file :
            data = line.split('\t')
            seq_genomic_list.append([int(data[1]), int(data[1]), data[3]])
    return seq_genomic_list

