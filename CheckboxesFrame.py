import tkinter as tk
from tkinter import RAISED, RIDGE, FLAT, GROOVE


class CheckboxesFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # the parent will be another frame
        self.parent = parent

        # frame configuration
        self.config(bg="lightseagreen", width=220, height=175)
        self.grid_propagate(0)

        # widgets for this frame
        self.segmentId_checkB = None
        self.headerId_checkB = None
        self.header_checkB = None
        self.base_seg_checkB = None
        self.trailer_checkB = None
        self.colCheckboxFrame = tk.Frame(self, bg='lightseagreen')
        self.colCheckboxFrame.grid(row=0, column=0, sticky='w')
        self.rowCheckboxFrame = tk.Frame(self, bg='lightseagreen')
        self.rowCheckboxFrame.grid(row=1, column=0, sticky='w')
        self.createCheckboxes()

    def createCheckboxes(self):
        self.segmentId_checkB = tk.Checkbutton(self.colCheckboxFrame,
                                               text="Segment IDs",
                                               command=lambda: self.update_checkbox_state("baseId"),
                                               variable=tk.IntVar(),
                                               indicatoron=0,
                                               offrelief=RAISED,
                                               overrelief=GROOVE,
                                               font=("Courier", 12))
        self.segmentId_checkB.grid(row=0, column=0, pady=9)
        self.header_checkB = tk.Checkbutton(self.rowCheckboxFrame,
                                            text="Header",
                                            command=lambda: self.update_checkbox_state("header"),
                                            variable=tk.IntVar(),
                                            indicatoron=0,
                                            offrelief=RAISED,
                                            overrelief=GROOVE,
                                            font=("Courier", 12)).grid(row=1, column=0, pady=9)
        self.base_seg_checkB = tk.Checkbutton(self.rowCheckboxFrame,
                                              text="Base",
                                              command=lambda: self.update_checkbox_state("base"),
                                              variable=tk.IntVar(),
                                              indicatoron=0,
                                              offrelief=RAISED,
                                              overrelief=GROOVE,
                                              font=("Courier", 12)).grid(row=1, column=1, pady=9)
        self.trailer_checkB = tk.Checkbutton(self.rowCheckboxFrame,
                                             text="Trailer",
                                             command=lambda: self.update_checkbox_state("trailer"),
                                             variable=tk.IntVar(),
                                             indicatoron=0,
                                             offrelief=RAISED,
                                             overrelief=GROOVE,
                                             font=("Courier", 12)).grid(row=1, column=2, pady=9)

    def update_checkbox_state(self, name):
        if not self.parent.checkbox_state[name]:
            self.parent.checkbox_state[name] = True
        else:
            self.parent.checkbox_state[name] = False
