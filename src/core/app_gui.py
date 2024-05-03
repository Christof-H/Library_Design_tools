import tkinter as tk
from functools import partial
from pathlib import Path

from models.interface import Interface
import core.gui_function as gf


def main_gui():
    # creating a dictionary to save all Entry widgets to store and recover user parameters
    entries_widgets = {}
    # creating a dictionary to save all values widgets to store and recover variable user parameters
    var_widgets = {}
    # creating a dictionary to stores parameters
    input_parameters = {}

    # creating the main window with a Notebook
    my_gui = Interface(tabs=True, dim_width=1000, dim_height=470)

    #######################################################################################
    #               creating of the different tabs in the Notebook
    #######################################################################################
    tab_param = my_gui.create_frame_in_notebook("  Parameters  ")
    tab_graphic = my_gui.create_frame_in_notebook("  Graphic result  ")
    tab_board = my_gui.create_frame_in_notebook("  Library details  ")

    #######################################################################################
    #               creating of the different Labelframe in the Parameters tab
    #######################################################################################

    labelframe_file = my_gui.create_labelframe(
        parent=tab_param,
        text="Files/Folders",
        column=0,
        row=0,
        columnspan=6,
    )
    labelframe_param = my_gui.create_labelframe(
        parent=tab_param,
        text="Library parameters",
        column=0,
        row=1,
        columnspan=6,
    )
    button_exit = my_gui.create_button(
        master=tab_param, text="Exit", column=5, row=2, command=my_gui.destroy
    )
    button_start_design = my_gui.create_button(
        master=tab_param,
        text="Start Libray Design",
        column=1,
        row=2,
        command=partial(
            gf.check_recover_settings, input_parameters, entries_widgets, var_widgets
        ),
    )

    #######################################################################################
    #                           File/Folder LabelFrame
    #######################################################################################

    #                    info image label (File/Folder LabelFrame)
    # --------------------------------------------------------------------------------------
    info_img_path = Path(__file__).absolute().parents[1].joinpath("resources/info.png")
    info_load_param, info_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path=info_img_path,
        resize_rate=4,
        column=0,
        row=0,
        padx=8,
    )
    info_chr_folder, chr_folder_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path=info_img_path,
        resize_rate=4,
        column=0,
        row=1,
        padx=8,
    )
    info_chr_name, chr_name_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path=info_img_path,
        resize_rate=4,
        column=0,
        row=2,
        padx=8,
    )
    info_output, output_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path=info_img_path,
        resize_rate=4,
        column=0,
        row=3,
        padx=8,
    )

    # --------------------------------------------------------------------------------------
    #                      Text labels (File/Folder LabelFrame)
    # --------------------------------------------------------------------------------------
    label_input_param = my_gui.create_label(
        labelframe_file,
        text="Load input parameters :",
        column=1,
        row=0,
        sticky=tk.W,
    )
    label_chr_path = my_gui.create_label(
        labelframe_file,
        text="Chromosome file path :",
        column=1,
        row=1,
        sticky=tk.W,
    )

    label_chr_name = my_gui.create_label(
        labelframe_file,
        text="Chromosome file name :",
        column=1,
        row=2,
        pady=5,
        sticky=tk.W,
    )
    label_output_path = my_gui.create_label(
        labelframe_file,
        text="Output folder path :",
        column=1,
        row=3,
        pady=5,
        sticky=tk.W,
    )
    # --------------------------------------------------------------------------------------
    #                      Entries (File/Folder LabelFrame)
    # --------------------------------------------------------------------------------------

    # Entry for inputs parameters :
    entry_input_param = my_gui.create_entry(
        master=labelframe_file, width=50, column=2, row=0
    )
    entry_input_param.config(state=tk.DISABLED)

    # Entry for chromosome file path :
    entry_chr_file = my_gui.create_entry(
        master=labelframe_file, width=50, column=2, row=1
    )
    entry_chr_file.config(state=tk.DISABLED)

    # Entry for chromosome file name
    entry_chr_name = my_gui.create_entry(
        master=labelframe_file, width=20, column=2, row=2, sticky=tk.W
    )
    entry_chr_name.config(state=tk.DISABLED)

    # Entry for output folder path
    entry_output = my_gui.create_entry(
        master=labelframe_file, width=50, column=2, row=3
    )
    entry_output.config(state=tk.DISABLED)

    # Add different entries to the widget dictionary :
    entries_widgets.update({"genomic_path": entry_chr_file})
    entries_widgets.update({"chromosome_file": entry_chr_name})
    entries_widgets.update({"output_folder": entry_output})

    # --------------------------------------------------------------------------------------
    #                      Buttons (File/Folder LabelFrame)
    # --------------------------------------------------------------------------------------
    # Button to choose input parameters file (filedialog) :
    button_open_file = my_gui.create_button(
        labelframe_file,
        text="Open file",
        column=3,
        row=0,
        padx=10,
        sticky=tk.EW,
        command=partial(gf.open_file_dialog, entry_input_param),
    )

    # Button to load and fill input parameters in the different entries:
    button_load_param = my_gui.create_button(
        labelframe_file,
        text="Load parameters",
        column=4,
        row=0,
        padx=10,
        command=partial(
            gf.button_load_parameters,
            entry_input_param,
            entries_widgets,
            var_widgets,
            input_parameters,
        ),
    )

    # Button to choose chromosome file (filedialog) :
    button_chr_path = my_gui.create_button(
        labelframe_file,
        text="Choose file",
        column=3,
        row=1,
        padx=10,
        sticky=tk.EW,
        command=partial(
            gf.open_dialog_display_chr_name, entry_chr_file, entry_chr_name
        ),
    )

    # Button to choose output folder to save outputs (filedialog) :
    button_output = my_gui.create_button(
        labelframe_file,
        text="Choose folder",
        column=3,
        row=3,
        padx=10,
        command=partial(gf.open_folder_dialog, entry_output),
    )

    #######################################################################################
    #                       Library parameters LabelFrame
    #######################################################################################

    #              info image label (Library parameters LabelFrame)
    # --------------------------------------------------------------------------------------
    info_design, info_design_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path=info_img_path,
        resize_rate=4,
        column=0,
        row=0,
        padx=8,
    )
    info_labelling, info_labelling_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path=info_img_path,
        resize_rate=4,
        column=0,
        row=3,
        padx=8,
    )
    info_nbr_rt, nbr_rt_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path=info_img_path,
        resize_rate=4,
        column=0,
        row=6,
        padx=8,
    )
    info_nbr_probe, nbr_probe_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path=info_img_path,
        resize_rate=4,
        column=4,
        row=0,
        padx=8,
    )
    info_total_loci, total_loci_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path=info_img_path,
        resize_rate=4,
        column=4,
        row=1,
        padx=8,
    )
    info_lib_start, lib_start_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path=info_img_path,
        resize_rate=4,
        column=4,
        row=2,
        padx=8,
    )
    info_univ_primer, univ_primer_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path=info_img_path,
        resize_rate=4,
        column=4,
        row=3,
        padx=8,
    )
    # --------------------------------------------------------------------------------------
    #                   Text labels (Library parameters LabelFrame)
    # --------------------------------------------------------------------------------------
    label_design_strategy = my_gui.create_label(
        labelframe_param,
        text="Library strategy design :",
        column=1,
        row=0,
        sticky=tk.W,
    )
    label_labelling_strategy = my_gui.create_label(
        labelframe_param,
        text="Labelling strategy :",
        column=1,
        row=3,
        sticky=tk.W,
    )
    label_nbr_rt = my_gui.create_label(
        labelframe_param,
        text="Number RTs or barcodes by probe :",
        column=1,
        row=6,
        sticky=tk.W,
    )
    label_nbr_probe = my_gui.create_label(
        labelframe_param,
        text="Number of probes by locus :",
        columnspan=2,
        column=5,
        row=0,
        sticky=tk.W,
    )
    label_loci = my_gui.create_label(
        labelframe_param,
        text="Number of total loci :",
        column=5,
        row=1,
        sticky=tk.W,
    )
    label_lib_start = my_gui.create_label(
        labelframe_param,
        text="Library starting coordinates (in bp) :",
        column=5,
        row=2,
        columnspan=3,
        sticky=tk.W,
    )
    # --------------------------------------------------------------------------------------
    #                   Separator (Library parameters LabelFrame)
    # --------------------------------------------------------------------------------------
    separator = my_gui.create_frame(master=labelframe_param, column=3, row=0, width=80)
    # --------------------------------------------------------------------------------------
    #                   Entries (Library parameters LabelFrame)
    # --------------------------------------------------------------------------------------
    # label for this entry = according to locus size (in bp)
    locus_size = tk.IntVar()
    entry_locus_size = my_gui.create_entry(
        master=labelframe_param,
        textvariable=locus_size,
        width=6,
        column=2,
        row=1,
        sticky=tk.W,
    )
    locus_size.set(20000)

    # label for this entry = Number of probes by locus
    nbr_probes = tk.IntVar()
    entry_nbr_probes_by_locus = my_gui.create_entry(
        master=labelframe_param,
        textvariable=nbr_probes,
        width=5,
        column=7,
        row=0,
        sticky=tk.W,
    )
    nbr_probes.set(100)

    # label for this entry = Library starting coordinates (in bp)
    start_lib = tk.IntVar()
    entry_lib_starting = my_gui.create_entry(
        master=labelframe_param,
        textvariable=start_lib,
        width=12,
        column=8,
        row=2,
        sticky=tk.W,
    )
    start_lib.set(8_800_000)

    # Add different entries to the widget dictionary :
    var_widgets.update({"resolution": locus_size})
    var_widgets.update({"nbr_probe_by_locus": nbr_probes})
    var_widgets.update({"start_lib": start_lib})

    # --------------------------------------------------------------------------------------
    #                  Radio button  (Library parameters LabelFrame)
    # --------------------------------------------------------------------------------------
    design_type = tk.StringVar()
    radio_locus_size = my_gui.create_radiobutton(
        master=labelframe_param,
        text="according to locus size (in bp) :",
        variable=design_type,
        value="locus_length",
        column=1,
        row=1,
        pady=5,
        sticky=tk.W,
        command=partial(gf.change_state_widget, entry_locus_size, design_type),
    )
    radio_nbr_probes = my_gui.create_radiobutton(
        master=labelframe_param,
        text="by number of probes by locus",
        variable=design_type,
        value="nbr_probes",
        column=1,
        row=2,
        pady=5,
        sticky=tk.W,
        command=partial(gf.change_state_widget, entry_locus_size, design_type),
    )
    design_type.set("locus_length")

    rts_bcd = tk.StringVar()
    radio_labelling_rts = my_gui.create_radiobutton(
        master=labelframe_param,
        text="direct labelling (use of RTs)",
        variable=rts_bcd,
        value="List_RT.csv",
        column=1,
        row=4,
        pady=5,
        sticky=tk.W,
    )
    radio_labelling_barcode = my_gui.create_radiobutton(
        master=labelframe_param,
        text="indirect labelling (use of bridges)",
        variable=rts_bcd,
        value="Barcodes.csv",
        column=1,
        row=5,
        pady=5,
        sticky=tk.W,
    )
    rts_bcd.set("List_RT.csv")

    # Add different radio button variables to the widget dictionary :
    var_widgets.update({"design_type": design_type})
    var_widgets.update({"bcd_rt_file": rts_bcd})

    # --------------------------------------------------------------------------------------
    #                      Spin boxes (File/Folder LabelFrame)
    # --------------------------------------------------------------------------------------
    # label for this spinbox = Number RTs or barcodes by probes
    nbr_rt_bcd = tk.IntVar()
    nbr_rt_bcd.set(3)
    spinbox_nbr_rt_bcd = my_gui.create_spinbox(
        master=labelframe_param,
        from_=1,
        to=5,
        textvariable=nbr_rt_bcd,
        column=2,
        row=6,
        width=3,
    )
    # label for this spinbox = Number of total loci
    nbr_loci = tk.IntVar()
    nbr_loci.set(20)
    spinbox_nbr_loci = my_gui.create_spinbox(
        master=labelframe_param,
        from_=1,
        to=50,
        textvariable=nbr_loci,
        column=6,
        row=1,
        width=5,
    )

    # Add different spinbox variables to the widget dictionary :
    var_widgets.update({"nbr_bcd_rt_by_probe": nbr_rt_bcd})
    var_widgets.update({"nbr_loci_total": nbr_loci})

    # --------------------------------------------------------------------------------------
    #                      Combobox (File/Folder LabelFrame)
    # --------------------------------------------------------------------------------------
    lis_univ_primer = ["primer1", "primer2", "primer3"]
    univ_primer = tk.StringVar()
    combo_univ_primer = my_gui.create_combobox(
        master=labelframe_param,
        values=lis_univ_primer,
        textvariable=univ_primer,
        width=40,
        columnspan=4,
        column=5,
        row=3,
        sticky=tk.W,
    )
    univ_primer.set("Choose universal primer couple")

    # Add combobox variables to the widget dictionary :
    var_widgets.update({"primer_univ": univ_primer})

    my_gui.mainloop()


if __name__ == "__main__":
    main_gui()
