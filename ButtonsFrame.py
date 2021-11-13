import tkinter as tk
from tkinter import messagebox

from Editor import *


class ButtonsFrame(tk.Frame):
    def __init__(self, parent, inputFieldsFrame, listbox, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # the parent will be another frame
        self.parent = parent
        self.listbox = listbox

        self.inputFrame = inputFieldsFrame
        self.colPositions = set()
        self.rowNumbers = set()
        self.col_errors = []
        self.row_errors = []
        self.dimensions = None
        self.text = None
        self.isReplacingDate = False

        # frame configuration
        self.config(bg="lightseagreen", padx=10, height=75, width=300)
        self.grid_propagate(0)

        # widgets for this frame
        self.replace_button = None
        self.clear_button = None
        # create widgets
        self.createButtons()

    def createButtons(self):
        self.replace_button = tk.Button(self, text="Replace", font=("Courier", 20), command=self.replaceClick) \
            .grid(row=0, column=0, padx=5, pady=5)
        self.clear_button = tk.Button(self, text="Clear", font=("Courier", 20), command=self.clearClick) \
            .grid(row=0, column=1, padx=5, pady=5)

    def clearClick(self):
        self.inputFrame.columns_to_mod_entry.delete(0, len(self.inputFrame.columns_to_mod_entry.get()))
        self.inputFrame.rows_to_mod_entry.delete(0, len(self.inputFrame.rows_to_mod_entry.get()))
        self.inputFrame.replacing_text_entry.delete(0, len(self.inputFrame.replacing_text_entry.get()))

    def replaceClick(self):
        self.replaceClickResetParameters()
        # upload a new file to the editor
        try:
            self.parent.editor.editNewFile(self.listbox.selected_filename)
            # grab dimensions of the text file
            self.dimensions = self.parent.editor.dimensions[0] - 1, self.parent.editor.dimensions[1] - 1
        except TypeError:
            messagebox.showerror("ERROR", "No file was selected from the file list.")
            return

        # update column positions and row positions based on the checkbox states
        if not self.invoke_col_checkbox_state(self.dimensions):
            self.col_errors = process_user_col_row_positions(self.inputFrame.columns_to_mod_entry.get(),
                                                             self.colPositions)
        if not self.invoke_row_checkbox_state(self.dimensions):
            self.row_errors = process_user_col_row_positions(self.inputFrame.rows_to_mod_entry.get(), self.rowNumbers)

        # print("Columns selected: " + str(self.colPositions))
        # print("Rows selected: " + str(self.rowNumbers))

        # check for user text entry errors
        self.text = self.inputFrame.replacing_text_entry.get()
        # check that text input length match number of column positions, returning true means an error
        if handle_user_text_length_error(self.text, self.colPositions):
            return

        # show error message if no row numbers are specified
        for name, value in {'column numbers': self.colPositions, 'row numbers': self.rowNumbers,
                            'text': self.text}.items():
            if len(value) == 0:
                messagebox.showerror("ERROR", "Make sure to specify the {}.".format(name))
                return
        # throws exceptions related to dimensions and user inputs
        self.checkDimensions()
        # try:
        # replace the text file text and create an output file in the output directory
        print(str(self.colPositions) + ":" + str(self.rowNumbers))
        if self.isReplacingDate:
            out_message = self.parent.editor.find_and_replace_date(self.inputFrame.date_mod_entry.get(),
                                                                   self.inputFrame.replacing_text_entry.get(),
                                                                   self.rowNumbers,
                                                                   min(self.colPositions))
            print(out_message)
            messagebox.showinfo('Message', out_message)
            self.isReplacingDate = False
        else:
            self.parent.editor.replaceText(self.colPositions, self.rowNumbers,
                                           self.inputFrame.replacing_text_entry.get())
            messagebox.showinfo('Message', 'Text replacement successful!\nFind output in the \'processed\' '
                                           'folder in the directory.')
        # except IndexError:
        #     messagebox.showerror("ERROR", "Make sure that the number of characters in the text "
        #                                   "field matches the number of column positions selected.")

    def replaceClickResetParameters(self):
        self.colPositions.clear()
        self.rowNumbers.clear()
        self.parent.editor = Editor()

    def invoke_col_checkbox_state(self, dimensions):
        for key, value in self.parent.checkbox_state.items():
            if value:
                if key == "baseId":
                    self.colPositions.update(set([num for num in range(21, 42)]))
                    return True
                if key == "date":
                    date = self.inputFrame.date_mod_entry.get()
                    try:
                        process_user_date_replace_input(date)
                        self.colPositions = process_user_date_col_input(self.inputFrame.columns_to_mod_entry.get())
                        self.isReplacingDate = True
                    except ValueError:
                        messagebox.showerror("ERROR", "Either Date or column entered was not valid.\n{}".format(date))
                    except AttributeError:
                        messagebox.showerror("ERROR", "Either the date or starting column position was not entered.")
        return False

    def invoke_row_checkbox_state(self, dimensions):
        changed_state = False
        for key, value in self.parent.checkbox_state.items():
            if value:
                if key == "header":
                    self.rowNumbers.add(1)
                    changed_state = True
                if key == "trailer":
                    self.rowNumbers.add(dimensions[1] + 1)
                    changed_state = True
                if key == "base":
                    self.rowNumbers.update(set([num for num in range(2, dimensions[1] + 1)]))
                    changed_state = True
        return changed_state

    # check to make sure the entry inputs are within the dimensions of the file
    # returns true if no errors are found
    def checkDimensions(self):
        row_errors = []
        for row in self.rowNumbers:
            if row - 1 < 0 or row - 1 > self.dimensions[1]:
                row_errors.append(row)
        for error in row_errors:
            self.rowNumbers.remove(error)
        if len(row_errors) > 0:
            messagebox.showerror("ERROR",
                                 "These inputted rows are not within the range of rows in the selected file:\n{} ".format(
                                     str(row_errors)) +
                                 "\nThe text replacement will not include these rows.")
            return False
        return True
