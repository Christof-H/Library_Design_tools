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
        locus_n: int = None,
        chr_name: str = None,
        start_seq: int = None,
        end_seq: int = None,
        primers_univ: list[str] = None,
        bcd_locus: str = None,
        seq_probe: list[str] = None,
    ):
        """Initializes a new instance of a locus

        Args:
            locus_n (int): Locus Number. Defaults to None.
            chr_name (str): Chromosome name. Defaults to None.
            start_seq (int): Locus start coordinates (in bp). Defaults to None.
            end_seq (int): Locus end coordinates (in bp). Defaults to None.
            primers_univ (list[str]): Names and sequences of universal primers in list form. Defaults to None.
            bcd_locus (str): Barcode or RT name. Defaults to None.
            seq_probe (list[str]): primary probes sequences in list form. Defaults to None.
        """

        self.locus_n = locus_n
        self.chr_name = chr_name
        self.start_seq = start_seq
        self.end_seq = end_seq
        self.primers_univ = primers_univ
        self.bcd_locus = bcd_locus
        self.seq_probe = seq_probe

    def __str__(self):
        string = f"Chr. Name : {self.chr_name}\n\
locus Number : {self.locus_n}\n\
bcd or RT for this locus : {self.bcd_locus}\n\
Locus start coordinates : {self.start_seq}\n\
Locus enf coordinates : {self.end_seq}\n"
        if self.primers_univ and self.seq_probe:
            string += f"Primer Univ Fw :{self.primers_univ[0]}\n\
Primer Univ Rev :{self.primers_univ[2]}\n\
Primary probe sequence exemple : {self.seq_probe[0]}"
        return string
