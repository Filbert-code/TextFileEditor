# Use Tkinter for python 2, tkinter for python 3
import tkinter as tk
import os
from tkinter import HORIZONTAL


class ListboxFrame(tk.Frame):
    def __init__(self, parent, editor, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # the parent will be another frame
        self.parent = parent
        self.editor = editor
        self.filenames = os.listdir(self.editor.file_input_path)
        self.selected_filename = None

        # frame configuration
        self.config(bg="lightseagreen", width=350, height=175)
        self.grid_propagate(0)

        # widgets for this frame
        self.listbox = None
        self.createListbox()
        self.update_self()

    def createListbox(self):
        self.yscrollbar = tk.Scrollbar(self)
        self.yscrollbar.grid(row=0, column=1, sticky='ns')
        self.xscrollbar = tk.Scrollbar(self, orient=HORIZONTAL)
        self.xscrollbar.grid(row=1, column=0, sticky='ew')
        self.listbox = tk.Listbox(self, font=("Courier", 12), yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set, height=8, width=33, activestyle='dotbox', bg='lightcyan', exportselection=False)
        self.listbox.grid(row=0, column=0)

        self.yscrollbar.config(command=self.listbox.yview)
        self.xscrollbar.config(command=self.listbox.xview)
        self.listbox.insert(1, *self.filenames)

    # update the selected-filename field
    def update_self(self):
        if len(self.listbox.curselection()) > 0:
            self.selected_filename = self.listbox.get(self.listbox.curselection()[0])

        new_filenames = os.listdir(self.editor.file_input_path)
        if self.filenames != new_filenames:
            self.listbox.delete(0, len(self.filenames) - 1)
            self.filenames = new_filenames
            self.listbox.insert(1, *self.filenames)

        self.parent.parent.after(1000, self.update_self)