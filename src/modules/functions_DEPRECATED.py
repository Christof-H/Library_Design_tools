class LocusDataClass:
    def __init__(
        self,
        locusN,
        sousRegionN="",
        regionN="",
        chrName="",
        startSeq="",
        endSeq="",
        primers_Univ="",
        codeLocus="",
        bcdLocus="",
        codeSousRegion="",
        bcdSousRegion="",
        seqProbe="",
    ):
        """Création de la Classe locus ou l'on va stocker toutes les infos concernant
les différents locus d'une même bibliothèque"""
        self.locusN = locusN
        self.sousRegionN = sousRegionN
        self.regionN = regionN
        self.chrName = chrName
        self.startSeq = int(startSeq)
        self.endSeq = int(endSeq)
        self.primers_Univ = primers_Univ
        self.codeLocus = codeLocus
        self.bcdLocus = bcdLocus
        self.codeSousRegion = codeSousRegion
        self.bcdSousRegion = bcdSousRegion
        self.seqProbe = seqProbe


# ---------------------------FUNCTIONS---------------------------

# Evaluation de la longueur des sondes primaires de toute la librairie
def Check_Length_Seq_Diff(librairy):
    minimal_length = 500
    maximal_length = 100
    for locus in librairy:
        for seq in locus.seqProbe:
            if len(seq.replace(" ", "")) < minimal_length:
                minimal_length = len(seq.replace(" ", ""))
            elif len(seq.replace(" ", "")) > maximal_length:
                maximal_length = len(seq.replace(" ", ""))
    difference_pourcentage = 100 - (minimal_length * 100 / maximal_length)
    difference_nbre = maximal_length - minimal_length
    print(f"Length of smaller primary sequence = {str(minimal_length)}-mer")
    print(f"Length of bigger primary sequence = {str(maximal_length)}-mer")
    print(f"Difference in percentage : {int(difference_pourcentage)}%")
    print(f"Difference in nucleotides : {difference_nbre}-mer")
    return int(difference_pourcentage), maximal_length


# Fonction permettant le complétion de nucléotides aléatoires pour des sequences dont la difference de taille est supérieure a 10%
def Completion(difference_pourcentage, Max_length, librairy, Max_diff_pourcent=10):
    # Max_diff_pourcent = pourcentage de difference maximal toléré, calculé à partir de la fonction Check_Length_Seq_Diff()
    # Max_length = provient normalement de la fonction Check_Length_Seq_Diff()
    # librairy = liste des locus sous forme de locusDataClass
    import random

    if difference_pourcentage >= Max_diff_pourcent:
        for locus in librairy:
            seq_completion = list()
            for seq in locus.seqProbe:
                diff_seq_with_max = Max_length - len(seq.replace(" ", ""))
                seq_added = ""
                for i in range(diff_seq_with_max):
                    seq_added = seq_added + random.choice("atgc")
                seq_completion.append(seq + " " + seq_added)
            locus.seqProbe = seq_completion
        print("-" * 70)
        print("Completion finished")
        print("-" * 70)
    else:
        print("-" * 70)
        print("No completion required")
        print("-" * 70)
