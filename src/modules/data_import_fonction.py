def universal_Primer_format(path : str) -> dict[str, str]:
    """Function for opening, formatting and storing universal primer sequences.

    Args:
        path (str): File path of universal primer couple

    Returns:
        dict[str, list(str)]: [description]
    """

    primerUniv={}
    with open(path, mode="r", encoding="utf-8") as file:
        for line in file:
            data = line.replace('\n','').split(',')
            primerUniv[data[0]] = [item for item in data[1:]]
    return primerUniv


def bcd_RT_format(path : str) -> list[str]:
    """Function for opening, formatting and storing barcode or RT sequences.

    Args:
        path (str): File path of Barcodes or RT

    Returns:
        list[list[str]]: [[name, sequence], ...]
    """

    bcd_RT_list = []
    with open(path, mode='r', encoding='utf-8') as file:
        for line in file:
            data = line.replace('\n', '').split(',')
            bcd_RT_list.append(data)
        return bcd_RT_list


def seq_genomic_format(path : str) -> list[str]:
    """Function for opening, formatting and storing genomic sequences.

    Args:
        path (str): File path of genomic sequences

    Returns:
        list[str]: [description]
    """

    seq_genomic_list = []
    with open(path, mode='r', encoding='UTF-8') as file :
        for line in file :
            data = line.split('\t')
            seq_genomic_list.append(data[1:4])
    return seq_genomic_list

