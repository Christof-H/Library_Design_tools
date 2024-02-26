class Locus:

    def __init__(
        self,
        locus_n,
        chr_name,
        start_seq,
        end_seq,
        primers_univ,
        bcd_locus,
        seq_probe
    ):
        """AI is creating summary for __init__

        Args:
            locus_n (int): Locus Number
            chr_name (str): Chromosome name
            start_seq (int): Locus start coordinates (in bp)
            end_seq (int): Locus end coordinates (in bp)
            primers_univ (list[str]): Names and sequences of universal primers in list form
            bcd_locus (str): Barcode or RT name
            seq_probe (list[str]): primary probes sequences in list form 
        """


        self.locus_n = locus_n
        self.chr_name = chr_name
        self.start_seq = start_seq
        self.end_seq = end_seq
        self.primers_univ = primers_univ
        self.bcd_ocus = bcd_locus
        self.seq_probe = seq_probe
