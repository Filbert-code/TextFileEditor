import re
from Editor import Editor

class EditorMenu:

    def __init__(self):
        self.text = None
        self.colPositions = set()
        self.rowNumbers = set()

    def run(self):
        in_menu = True
        while in_menu:
            self.menu()
            in_menu = self.menu_input()

        editor = Editor("testing" + ".txt")
        # for line in editor.file_string_array:
        #     print(line)
        # print(editor.dimensions)
        editor.replaceText(self.colPositions, self.rowNumbers, self.text)
        print("\nFile editing operation complete.\n\n")

    def menu(self):
        print("\n-----------WELCOME-TO-THE-MOD-ZONE-----------\n")
        print("What we need from you:")
        print("All the column positions (starting from 1) that need to be modified...")
        print("All the row numbers (starting from 1) that need these columns positions modified...")
        print("And the text that will replace these rows.\n")
        print("If you put in 7 column positions to be modified, make sure your text has 7 characters...")
        print("or shit will hit the fan")
        print("\n" + "Have fun! :)\n")

    def menu_input(self):
        # array of column positions
        inputColPositions = input("Column positions (starting from 1): ")
        # get rid of white space, invalid characters and keeps any usable inputs from the user and returns the errors
        col_input_errors = self.process_user_col_row_positions(inputColPositions, self.colPositions)
        inputRowNumbers = input("Row numbers (starting from 1): ")
        row_input_errors = self.process_user_col_row_positions(inputRowNumbers, self.rowNumbers)
        print(self.colPositions)
        print(self.rowNumbers)
        self.text = input("Text ({} Characters): ".format(len(self.colPositions)))

        # check if the user wants to continue if errors were found
        if self.handle_user_col_row_input_errors(col_input_errors, "column") != 'y':
            print("Restarting...")
            return True
        if self.handle_user_col_row_input_errors(row_input_errors, "row") != 'y':
            print("Restarting...")
            return True
        if self.handle_user_text_length_error() == 1:
            print("Restarting...")
            return True
        return False


    # process user input by checking if the input matches a regular expression. If no matches are found, the string is
    # put into a error array and returned at the end
    def process_user_col_row_positions(self, positions, output):
        errors = []
        inputRegex = "(\d*)|(\d*-\d*)"
        for position in positions.split(","):
            # trimming white space from the user input before matching regex
            pos = position.strip()
            match = re.match(inputRegex, pos)
            if match.group(0) == '':
                errors.append(pos)
            else:
                if "-" in pos:
                    posSplit = pos.split("-")
                    # range needs to use ints, so we convert from string
                    int_split = [int(num) for num in posSplit]
                    for i in range(min(int_split), max(int_split) + 1):
                        output.add(i)
                else:
                    output.add(int(pos))
        return errors

    def handle_user_col_row_input_errors(self, errors, data_type):
        if len(errors) > 0:
            print("There were some invalid {} numbers: ".format(data_type) + str(errors))
            return input("Would you still like to continue excluding these invalid numbers? (y/n) ")
        return 'y'

    def handle_user_text_length_error(self):
        if len(self.text) != len(self.colPositions):
            print("Length of inputted text does not match the number of column positions given:")
            print("{}: length {}".format(self.text, len(self.text)))
            print("Col Positions: {}: length {}".format(self.colPositions, len(self.colPositions)))
            return 1
        return 0




