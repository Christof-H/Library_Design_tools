import tkinter as tk

from models.interface import Interface


def main_gui():
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
        parent=tab_param, text="Files/Folders", height=200
    )
    labelframe_param = my_gui.create_labelframe(
        parent=tab_param, text="Library parameters", height=400
    )
    #######################################################################################
    #                           File/Folder LabelFrame
    #######################################################################################

    #                    info image label (File/Folder LabelFrame)
    # --------------------------------------------------------------------------------------
    info_load_param, info_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=0,
        padx=8,
    )
    info_chr_folder, chr_folder_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=1,
        padx=8,
    )
    info_chr_name, chr_name_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=2,
        padx=8,
    )
    info_output, output_img = my_gui.create_label_img(
        master=labelframe_file,
        image_path="../resources/info.png",
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
    entry_input = my_gui.create_enty(master=labelframe_file, width=50, column=2, row=0)
    entry_chr_folder = my_gui.create_enty(
        master=labelframe_file, width=50, column=2, row=1
    )
    entry_chr_name = my_gui.create_enty(
        master=labelframe_file, width=20, column=2, row=2, sticky=tk.W
    )
    entry_output = my_gui.create_enty(master=labelframe_file, width=50, column=2, row=3)

    # --------------------------------------------------------------------------------------
    #                      Buttons (File/Folder LabelFrame)
    # --------------------------------------------------------------------------------------
    button_open_file = my_gui.create_button(
        labelframe_file, text="Open file", column=3, row=0, padx=10, sticky=tk.EW
    )
    button_load_param = my_gui.create_button(
        labelframe_file, text="Load parameters", column=4, row=0, padx=10
    )
    button_load_param = my_gui.create_button(
        labelframe_file, text="Choose file", column=3, row=1, padx=10, sticky=tk.EW
    )
    button_output = my_gui.create_button(
        labelframe_file, text="Choose folder", column=3, row=3, padx=10
    )
    #######################################################################################
    #                       Library parameters LabelFrame
    #######################################################################################

    #              info image label (Library parameters LabelFrame)
    # --------------------------------------------------------------------------------------
    info_design, info_design_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=0,
        padx=8,
    )
    info_labelling, info_labelling_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=3,
        padx=8,
    )
    info_nbr_rt, nbr_rt_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=0,
        row=6,
        padx=8,
    )
    info_nbr_probe, nbr_probe_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=3,
        row=0,
        padx=8,
    )
    info_total_loci, total_loci_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=3,
        row=1,
        padx=8,
    )
    info_lib_start, lib_start_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=3,
        row=2,
        padx=8,
    )
    info_univ_primer, univ_primer_img = my_gui.create_label_img(
        master=labelframe_param,
        image_path="../resources/info.png",
        resize_rate=4,
        column=3,
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
        column=4,
        row=0,
        sticky=tk.W,
    )
    label_loci = my_gui.create_label(
        labelframe_param,
        text="Number of total loci :",
        column=4,
        row=1,
        sticky=tk.W,
    )
    label_lib_start = my_gui.create_label(
        labelframe_param,
        text="Library starting coordinates (in bp) :",
        column=4,
        row=2,
        sticky=tk.W,
    )
    # --------------------------------------------------------------------------------------
    #                  Radio button  (Library parameters LabelFrame)
    # --------------------------------------------------------------------------------------
    design_type = tk.StringVar()
    radio_locus_size = my_gui.create_radiobutton(
        master=labelframe_param,
        text="according to locus size (in kb) :",
        variable=design_type,
        value="locus_length",
        column=1,
        row=1,
        pady=5,
        sticky=tk.W,
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
    )
    design_type.set("locus_length")

    rts_bcd = tk.StringVar()
    radio_labelling_rts = my_gui.create_radiobutton(
        master=labelframe_param,
        text="direct labelling (use of Readout probes)",
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

    # --------------------------------------------------------------------------------------
    #                   Entries (Library parameters LabelFrame)
    # --------------------------------------------------------------------------------------
    entry_locus_size = my_gui.create_enty(
        master=labelframe_param, width=5, column=2, row=1, sticky=tk.W
    )
    entry_locus_size.insert(0, 3.5)

    entry_nbr_probes_by_locus = my_gui.create_enty(
        master=labelframe_param, width=5, column=5, row=0, sticky=tk.W
    )
    entry_nbr_probes_by_locus.insert(0, 100)

    entry_lib_starting = my_gui.create_enty(
        master=labelframe_param, width=12, column=5, row=2, sticky=tk.W
    )
    entry_lib_starting.insert(0, 8_800_000)

    # --------------------------------------------------------------------------------------
    #                      Spin boxes (File/Folder LabelFrame)
    # --------------------------------------------------------------------------------------
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
    nbr_loci = tk.IntVar()
    nbr_loci.set(20)
    spinbox_nbr_rt_bcd = my_gui.create_spinbox(
        master=labelframe_param,
        from_=1,
        to=50,
        textvariable=nbr_loci,
        column=5,
        row=1,
        width=5,
    )

    # --------------------------------------------------------------------------------------
    #                      Comboboxe (File/Folder LabelFrame)
    # --------------------------------------------------------------------------------------
    lis_univ_primer = ["primer1", "primer2", "primer3"]
    univ_primer = tk.StringVar()
    combo_univ_primer = my_gui.create_combobox(
        master=labelframe_param,
        values=lis_univ_primer,
        textvariable=univ_primer,
        width=40,
        column=4,
        row=3,
        sticky=tk.W,
    )
    univ_primer.set("Choose universal primer couple")

    my_gui.mainloop()


if __name__ == "__main__":
    main_gui()
