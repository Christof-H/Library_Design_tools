class InvalidNbrLocusException(Exception):
    """Handles the exception if the number of barcodes or RTs available is insufficient 
    in relation to the total number of loci.

    Args:
        nbr_locus (int): The total number of loci.
        nbr_bcd_rt (int): The number of available barcodes or RTs.
        type_bcd_rt (str): The type of barcodes or RTs (e.g., "barcodes" or "RTs").
    """

    def __init__(self, nbr_locus, nbr_bcd_rt, type_bcd_rt):
        msg = f"\n{'-'*70}\n Number of {type_bcd_rt} insufficient : {nbr_bcd_rt} {type_bcd_rt}\
 for {nbr_locus} loci"
        super().__init__(msg)
