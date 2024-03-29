import matplotlib.pyplot as plt
from pathlib import Path


def display_locus_info(
    list_info_to_plot: list[int],
    folder: Path,
    design_type: str,
    locus_length: int,
    nbr_probes_by_locus: int,
):
    if design_type == "locus_length":
        titre = f"Number of probes per locus ({locus_length/1000}Kb)"
        y_label_title = "Number of probes"
        list_to_plot = list_info_to_plot
    else:
        titre = f"Length of locus ({nbr_probes_by_locus} probes/locus)"
        y_label_title = "Length (Kb)"
        list_to_plot = [x / 1000 for x in list_info_to_plot]

    y_min = min(list_to_plot)
    y_max = max(list_to_plot)
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(list_to_plot)), list_to_plot)
    plt.xlabel("Locus")
    plt.ylabel(y_label_title)
    plt.title(titre)
    plt.xticks(range(len(list_to_plot)), list(range(1, len(list_to_plot) + 1)))
    plt.savefig(fname=folder.joinpath("plot.png"))
    plt.show()
