import tkinter as tk
from tkinter import W, RAISED, E
from Editor import *


class InputFieldsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # the parent will be another frame
        self.parent = parent

        self.characters_needed = 0

        # frame configuration
        self.config(bg="blue", padx=5, height=175, width=530)
        self.grid_propagate(0)

        # widgets for this frame
        self.columns_to_mod_label = None
        self.columns_to_mod_entry = None
        self.rows_to_mod_label = None
        self.rows_to_mod_entry = None
        self.replacing_text_label = None
        self.replacing_text_entry = None
        self.text_length_info_label = None
        # create widgets
        self.createTextFields()
        # update the character count
        self.update_self()

    def createTextFields(self):
        self.columns_to_mod_label = tk.Label(self, text="Columns to Modify:", font=("Courier", 12), relief=RAISED) \
                                      .grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.columns_to_mod_entry = tk.Entry(self, font=("Courier", 12), width=30, bg='lightcyan', disabledbackground='slategrey')
        self.columns_to_mod_entry.grid(row=0, column=1)

        self.date_mod_label = tk.Label(self, text="Date to Modify:", font=("Courier", 12), relief=RAISED)
        self.date_mod_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.date_mod_entry = tk.Entry(self, font=("Courier", 12), width=30, bg='lightcyan', disabledbackground='slategrey', state='disabled')
        self.date_mod_entry.grid(row=1, column=1, padx=5, pady=10, sticky='e')

        self.rows_to_mod_label = tk.Label(self, text="Rows to Modify:", font=("Courier", 12), relief=RAISED) \
                                   .grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.rows_to_mod_entry = tk.Entry(self, font=("Courier", 12), width=30, bg='lightcyan', disabledbackground='slategrey')
        self.rows_to_mod_entry.grid(row=2, column=1)

        self.replacing_text_label = tk.Label(self, text="Replacing Text:", font=("Courier", 12), relief=RAISED) \
                                      .grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.replacing_text_entry = tk.Entry(self, font=("Courier", 12), width=30, bg='lightcyan')
        self.replacing_text_entry.grid(row=3, column=1)

        self.text_length_info_label = tk.Label(self, text="Characters Needed: 0", bg="lightseagreen")
        self.text_length_info_label.grid(sticky=W, row=4, column=1)

# update the character count label
    def update_self(self):
        self.text_length_info_label.config(text="Characters Needed: {}".format(str(self.characters_needed)),
                                           font=("Courier", 12))
        self.changeEntryState()

        # update the text_length_info_label
        output = set()
        try:
            if not self.columns_to_mod_entry.cget('state') == 'disabled':
                process_user_col_row_positions(self.columns_to_mod_entry.get(), output)
                self.characters_needed = len(output) - len(self.replacing_text_entry.get())
            else:
                self.characters_needed = self.parent.characters_needed_state - len(self.replacing_text_entry.get())
        except:
            pass

        self.parent.parent.after(100, self.update_self)


    def changeEntryState(self):
        # change the entry from NORMAL to DISABLED based on the checkbox state
        # if it adds up to 3, then all states are true and the entry stays NORMAL, otherwise the entry is DISABLED
        row_state_addition = 0
        for key, value in self.parent.checkbox_state.items():
            if key == "baseId":
                if value:
                    self.columns_to_mod_entry.config(state=tk.DISABLED)
                    self.parent.characters_needed_state = len(range(21, 42))
                else:
                    self.columns_to_mod_entry.config(state=tk.NORMAL)
            elif key == "header" or key == "base" or key == "trailer":
                if not value:
                    row_state_addition += 1

        if row_state_addition != 3:
            self.rows_to_mod_entry.config(state=tk.DISABLED)
        else:
            self.rows_to_mod_entry.config(state=tk.NORMAL)

