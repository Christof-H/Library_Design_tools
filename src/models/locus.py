import random

from models.invalidNbrLocusException import InvalidNbrLocusException


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


class Locus:
    """A class for storing all the information about a specific locus

    Attributes:
    -----------
        locus_n (int):
            Locus Number. Defaults to None.
        chr_name (str):
            Chromosome name. Defaults to None.
        start_seq (int):
            Locus start coordinates (in bp). Defaults to None.
        end_seq (int):
            Locus end coordinates (in bp). Defaults to None.
        primers_univ (list[str]):
            Names and sequences of universal primers in list form. Defaults to None.
        bcd_locus (str):
            Barcode or RT name. Defaults to None.
        seq_probe (list[str]):
            primary probes sequences in list form. Defaults to None.
    """

    def __init__(
        self,
        primers_univ: list[str],
        locus_n: int = None,
        chr_name: str = None,
        resolution: int = None,
        nbr_probe_by_locus: int = None,
        design_type: str = None,
        start_seq: int = None,
        end_seq: int = None,
        bcd_locus: str = None,
        seq_probe: list[str] = None,
    ):
        """Initializes a new instance of a locus

        Args:
            locus_n (int): Locus Number. Defaults to None.
            chr_name (str): Chromosome name. Defaults to None.
            resolution (int): length of Locus
            nbr_probe_by_locus (int): number of probes by Locus
            start_seq (int): Locus start coordinates (in bp). Defaults to None.
            end_seq (int): Locus end coordinates (in bp). Defaults to None.
            primers_univ (list[str]): Names and sequences of universal primers in list form. Defaults to None.
            bcd_locus (str): Barcode or RT name. Defaults to None.
            seq_probe (list[str]): primary probes sequences in list form. Defaults to None.
        """

        self.locus_n = locus_n
        self.chr_name = chr_name
        self.resolution = resolution
        self.nbr_probe_by_locus = nbr_probe_by_locus
        self.design_type = design_type
        self.start_seq = start_seq
        self.end_seq = end_seq
        self.primers_univ = primers_univ
        self.bcd_locus = bcd_locus
        self.seq_probe = seq_probe

    def add_seq(self, list_seq: list[list[str]]) -> None:
        """Add the list of sequence to the Locus

        Args:
            list_seq (list[str]): A list of sequence
        """
        self.seq_probe = list_seq

    def check_nbr_probes(
        self, list_seq: list[list[int, int, str]]
    ) -> list[list[int, int, str]]:
        """Checks the number of primary sequences for the locus,
        and mixes and reduces the number of sequences if the maximum limit is reached.

        Args:
            list_seq (list[list[str]):
                A list of sequence : [[80000, 80020, 'CGATCGTGATGCTAGCATGT'], ...]

        Returns:
            (list[list[str]):
                A list of sequence reduced: [[80000, 80020, 'CGATCGTGATGCTAGCATGT'], ...]
        """
        if len(list_seq) > self.nbr_probe_by_locus:
            random.shuffle(list_seq)
            list_seq = list_seq[: self.nbr_probe_by_locus]
        return sorted(list_seq)

    def recover_genomic_seq(
        self,
        locus: int,
        nbr_loci_total: int,
        start_lib: int,
        seq_list_reduced: list[list[str]],
    ) -> tuple[list[str], int, int]:
        """Recover genomic sequences based on locus number ( = coordinates)

        Args:
            locus (int):
                Locus number
            seq_list_reduced (list[list[str]]):
                list of all sequences for the librairy

        Returns:
            tuple[list[str], int, int]: list sequence for the specific Locus, Locus start coordinates, Locus end coordinates
        """
        if self.design_type == "locus_length":
            # Calculation of start and end coordinates for each locus
            start_positions = [
                start_lib + x * self.resolution for x in range(nbr_loci_total)
            ]
            end_positions = [
                start_lib + (x + 1) * self.resolution for x in range(nbr_loci_total)
            ]
            temp = []
            for seq in seq_list_reduced:
                if (start_positions[locus - 1] <= seq[0]) and (
                    seq[1] < end_positions[locus - 1]
                ):
                    temp.append(seq)
                else:
                    pass

            final_seq_list = self.check_nbr_probes(temp)
            start = start_positions[
                locus - 1
            ]  # to be more precise : final_seq_list[0][0]
            end = end_positions[locus - 1]  # to be more precise : final_seq_list[-1][1]
            return [x[2] for x in final_seq_list], start, end

        elif self.design_type == "nbr_probes":
            final_seq_list = seq_list_reduced[
                (locus - 1)
                * self.nbr_probe_by_locus : (locus * self.nbr_probe_by_locus)
            ]
            start = final_seq_list[0][0]
            end = final_seq_list[-1][1]
            final_seq = [x[2] for x in final_seq_list]
        return final_seq, start, end

    def __str__(self):
        string = f"Chr. Name : {self.chr_name}\n\
locus Number : {self.locus_n}\n\
bcd or RT for this locus : {self.bcd_locus}\n\
Locus start coordinates : {self.start_seq}\n\
Locus end coordinates : {self.end_seq}\n"
        if self.primers_univ and self.seq_probe:
            string += f"Primer Univ Fw :{self.primers_univ[0]}\n\
Primer Univ Rev :{self.primers_univ[2]}\n\
Primary probe sequence exemple : {self.seq_probe[0]}"
        return string
