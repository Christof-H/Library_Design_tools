import random
from models.locus import Locus


class Library:
    """Library store a clooection of Locus

    Attributes:
    -----------
    total_loci (list[Locus]):
        collection a all Locus for this library

    Methods:
    --------
    add_locus(Locus):
        add a locus in the Locus collection (total_loci)
    check_length_seq_diff:
        Compare length sequences in all Locus of the Library

    """

    def __init__(self) -> None:
        self.total_loci = None

    def add_locus(self, locus: Locus):
        """add a locus in the Locus collection (total_loci)

        Args:
            locus (Locus):
                A Locus object
        """
        if self.total_loci is None:
            self.total_loci = []
        self.total_loci.append(locus)

    def check_length_seq_diff(self) -> tuple[int, int, int, int]:
        """Evaluation of the length (min, max) of the primary probes of the entire library and
          calculation of the percentage difference

        Returns:
            tuple[int, int, int, int]:
                minimal probe size
                maximum probe size
                difference in nucleutodes between the smallest and largest probe
                difference in size expressed as a percentage
        """
        minimal_length = None
        maximal_length = None
        for locus in self.total_loci:
            for seq in locus.seq_probe:
                if not minimal_length and not maximal_length:
                    minimal_length = len(seq.replace(" ", ""))
                    maximal_length = len(seq.replace(" ", ""))
                elif len(seq.replace(" ", "")) < minimal_length:
                    minimal_length = len(seq.replace(" ", ""))
                elif len(seq.replace(" ", "")) > maximal_length:
                    maximal_length = len(seq.replace(" ", ""))
        difference_percentage = 100 - (minimal_length * 100 / maximal_length)
        difference_nbre = maximal_length - minimal_length
        return minimal_length, maximal_length, difference_nbre, difference_percentage

    def completion(
        self, difference_percentage: int, max_length: int, max_diff_percent: int = 10
    ) -> None:
        """Random nucleotide completion function for sequences with too large a size difference (default=10%)

        Args:
            difference_percentage (int):
                difference in size between primary probes (for all Locus) expressed as a percentage
            max_length (int):
                maximum size between all the primary probe sequences of all Locus
            max_diff_percent (int, optional):
                maximum percentage difference in size allowed Defaults to 10.
        """

        if difference_percentage >= max_diff_percent:
            for locus in self.total_loci:
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
