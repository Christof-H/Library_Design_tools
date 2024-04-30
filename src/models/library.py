import random
import copy
import re

from models.locus import Locus


def recover_chr_name(chr_file_path):
    match = re.match(r"\S*(chr\w+)\.bed$", chr_file_path)
    if match:
        return match.group(1)


class Library:

    def __init__(self, parameters: dict[str, str | int]) -> None:
        self.start_lib = parameters["start_lib"]
        self.nbr_loci_total = parameters["nbr_loci_total"]
        self.max_diff_percent = parameters["max_diff_percent"]
        self.design_type = parameters["design_type"]
        self.loci_list = None

        self.chromosome_name = recover_chr_name(parameters["chromosome_file"])

    def add_locus(self, locus: Locus):
        """add a locus in the Locus collection (total_loci)

        Args:
            locus (Locus):
                A Locus object
        """
        if self.loci_list is None:
            self.loci_list = []
        self.loci_list.append(locus)

    def reduce_list_seq(
        self,
        seq_list: list[int, int, str],
        resolution: int,
        nbr_probe_by_locus: int,
    ) -> list[list[int, int, str]]:
        """Reduces the list of genomic sequences to library coordinates only to avoid
        iterating over all the genomic sequences of the chosen chromosome each time.

        Args:
            seq_list (list[list[str]]):
                list of genomic sequences with coordinates, based on target chromosome.
                [[80000, 80020, 'CGATCGTGATGCTAGCATGT'], ...]
            resolution (int):
                length of the Locus
            nbr_probe_by_locus (int):
                number of probes in a Locus

        Returns:
            (list[list[str]):
                A list of sequence reduced: [[80000, 80020, 'CGATCGTGATGCTAGCATGT'], ...]
        """
        list_seq_genomic_reduced = []
        if self.design_type == "locus_length":
            for seq in seq_list:
                if int(seq[0]) >= self.start_lib and int(seq[1]) <= (
                    self.start_lib + (self.nbr_loci_total * resolution)
                ):
                    list_seq_genomic_reduced.append(seq)
        elif self.design_type == "nbr_probes":
            for seq in seq_list:
                if self.start_lib <= int(seq[0]) and len(list_seq_genomic_reduced) < (
                    self.nbr_loci_total * nbr_probe_by_locus
                ):
                    list_seq_genomic_reduced.append(seq)
        return list_seq_genomic_reduced

    def add_rt_bcd_to_primary_seq(
        self, bcd_rt_list: list[list[str]], parameters: dict[str, str | int]
    ) -> None:
        """Add the rt/bcd sequences on either side of the genomic sequence according to the locus and the
        number of sites for oligo imaging..

        Args:
            bcd_rt_list (list[list[str]]):
                list of rt/barcode (name, sequence)
            parameters (dict[str, str | int]):
                dictionary with parameters for library design
        """
        count = 0
        for locus in self.loci_list:
            seq_with_bcd = []
            bcd_rt_seq = bcd_rt_list[count][1]
            locus.bcd_locus = bcd_rt_list[count][0]

            for genomic_seq in locus.seq_probe:
                if parameters["nbr_bcd_rt_by_probe"] == 2:
                    seq_with_bcd.append(f"{bcd_rt_seq} {genomic_seq} {bcd_rt_seq}")
                elif parameters["nbr_bcd_rt_by_probe"] == 3:
                    seq_with_bcd.append(f"{bcd_rt_seq} {genomic_seq} {bcd_rt_seq * 2}")
                elif parameters["nbr_bcd_rt_by_probe"] == 4:
                    seq_with_bcd.append(
                        f"{bcd_rt_seq * 2} {genomic_seq} {bcd_rt_seq * 2}"
                    )
                elif parameters["nbr_bcd_rt_by_probe"] == 5:
                    seq_with_bcd.append(
                        f"{bcd_rt_seq * 3} {genomic_seq} {bcd_rt_seq * 2}"
                    )
            count += 1
            locus.seq_probe = seq_with_bcd

    def add_univ_primer_each_side(self) -> None:
        """Add the forward and reverse primer sequences on either side of all primary probe loci sequences ."""
        for locus in self.loci_list:
            p_fw = copy.deepcopy(locus.primers_univ[1])
            p_rev = copy.deepcopy(locus.primers_univ[3])
            temp = [f"{p_fw} {x} {p_rev}" for x in locus.seq_probe]
            locus.seq_probe = temp

    def check_length_seq_diff(self) -> tuple[int, int, int, int]:
        """Evaluation of the length (min, max) of the primary probes of the entire library and
          calculation of the percentage difference

        Returns:
            tuple[int, int, int, int]:
                minimal probe size
                maximum probe size
                difference in nucleotides between the smallest and largest probe
                difference in size expressed as a percentage
        """
        minimal_length = None
        maximal_length = None
        for locus in self.loci_list:
            for seq in locus.seq_probe:
                if not minimal_length and not maximal_length:
                    minimal_length = len(seq.replace(" ", ""))
                    maximal_length = len(seq.replace(" ", ""))
                elif len(seq.replace(" ", "")) < minimal_length:
                    minimal_length = len(seq.replace(" ", ""))
                elif len(seq.replace(" ", "")) > maximal_length:
                    maximal_length = len(seq.replace(" ", ""))
        difference_percentage = 100 - (minimal_length * 100 / maximal_length)
        difference_nbr = maximal_length - minimal_length
        return minimal_length, maximal_length, difference_nbr, difference_percentage

    def completion(self, difference_percentage: int, max_length: int) -> None:
        """Random nucleotide completion function for sequences with too large a size difference (default=10%)

        Args:
            difference_percentage (int):
                difference in size between primary probes (for all Locus) expressed as a percentage
            max_length (int):
                maximum size between all the primary probe sequences of all Locus
        """

        if difference_percentage >= self.max_diff_percent:
            for locus in self.loci_list:
                seq_completion = []
                for seq in locus.seq_probe:
                    diff_seq_with_max = max_length - len(seq.replace(" ", ""))
                    seq_added = ""
                    for i in range(diff_seq_with_max):
                        seq_added = seq_added + random.choice("atgc")
                    seq_completion.append(seq + " " + seq_added)
                locus.seq_probe = seq_completion
            print("-" * 70)
            print("Completion finished")
            print("-" * 70)
        else:
            print("-" * 70)
            print("No completion required")
            print("-" * 70)

    def recover_loci_probes_length_info(self) -> list[int]:
        """Retrieves the number of probes per locus, or the size of each locus depending on the drawing type.

        Returns:
            list_info (list[int]): list of locus length or number of probes
        """
        list_info = []
        for locus in self.loci_list:
            if self.design_type == "locus_length":
                list_info.append(len(locus.seq_probe))
            else:
                list_info.append((locus.end_seq - locus.start_seq))
        return list_info
