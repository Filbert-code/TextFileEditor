# Use Tkinter for python 2, tkinter for python 3
import tkinter as tk
from tkinter import W, E

from InputFieldsFrame import InputFieldsFrame
from CheckboxesFrame import CheckboxesFrame
from ButtonsFrame import ButtonsFrame
from ListboxFrame import ListboxFrame
from Editor import Editor


class EditorGui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # parent is the root
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # configurations for the outer-most frame
        self.parent = parent
        self.parent.title("Metro-2 Text Replacement Tool")
        self.parent.maxsize(1100, 250)
        self.parent.minsize(1100, 250)
        self.config(bg='lightseagreen', width=1100, height=250)
        self.grid(row=0, column=0)
        self.grid_propagate(0)

        # states
        self.checkbox_state = {
            "baseId": False,
            "date": False,
            "header": False,
            "base": False,
            "trailer": False,
        }
        # tracks the number of characters the user needs to enter into the text field
        self.characters_needed_state = 0

        # create an Editor instance
        self.editor = Editor()

        # creating sub-frames
        self.listBox = ListboxFrame(self, self.editor)
        self.listBox.grid(row=1, column=2)
        self.inputFieldsFrame = InputFieldsFrame(self, self.listBox)
        self.inputFieldsFrame.grid(row=1, column=0)
        self.checkBoxesFrame = CheckboxesFrame(self)
        self.checkBoxesFrame.grid(row=1, column=1)
        self.buttonsFrame = ButtonsFrame(self, self.inputFieldsFrame, self.listBox)
        self.buttonsFrame.grid(sticky=E, row=2, column=0)

    #     self.states_debugger()
    #
    # def states_debugger(self):
    #     print(str(self.checkbox_state))
    #     self.parent.after(1000, self.states_debugger)



if __name__ == "__main__":
    root = tk.Tk()
    EditorGui(root)
    root.mainloop()