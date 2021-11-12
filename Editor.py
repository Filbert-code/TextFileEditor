import os
import re

# process user input by checking if the input matches a regular expression. If no matches are found, the string is
# put into a error array and returned at the end
import tkinter.messagebox


def process_user_col_row_positions(positions, output):
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

#
def process_user_date_col_input(position):
    inputRegex = "\d.*"
    match = re.match(inputRegex, position)
    if match.group(0) == '':
        raise ValueError
    else:
        return set([num for num in range(int(position), int(position) + 8)])

# check the user inputted date to make sure it's properly formatted
# return true if no errors are found
def process_user_date_replace_input(date):
    inputRegex = "\d{8}"
    match = re.match(inputRegex, date)
    print("date: {}...match: {}".format(date, match))
    if match.group(0) != date:
        raise ValueError



def handle_user_col_row_input_errors(errors, data_type):
    if len(errors) > 0:
        print("There were some invalid {} numbers: ".format(data_type) + str(errors))
        return input("Would you still like to continue excluding these invalid numbers? (y/n) ")
    return 'y'


def handle_user_text_length_error(text, colPositions):
    if len(text) != len(colPositions):
        tkinter.messagebox.showerror('ERROR', "Length of inputted text does not match the number of column positions given.")
        return True
    return False

class Editor:

    def __init__(self):
        self.filename = None
        self.path = None  # application path
        self.file_input_path = None  # input file path
        self.dimensions = None  # 1-indexed
        self.file_string_array = []
        self.createInputFileDirectory()

    def editNewFile(self, filename):
        self.filename = filename
        self.parseFile()
        self.findFileDimensions()

    # convert the text file into a string array
    def parseFile(self):
        with open(self.file_input_path + self.filename) as file:
            self.file_string_array = file.readlines()
            self.file_string_array = [line.rstrip() for line in self.file_string_array]

    # get the number of cols and rows
    def findFileDimensions(self):
        max_string_length = 0
        for string in self.file_string_array:
            if len(string) > max_string_length:
                max_string_length = len(string)
        # dimensions are in 1-indexed form (similar to how it would be viewed in a text editor)
        self.dimensions = (max_string_length + 1, len(self.file_string_array))

    # replace the characters in the indicated column positions with the new text in the string array
    def replaceText(self, columns_to_edit, rows_to_edit, text):
        # column numbers get 0-indexed in the mapping process
        textColumnMapping = self.mapTextToColumns(columns_to_edit, text)
        for row_num in rows_to_edit:
            # grab the row that needs to be updated, subtract 1 because rows_to_edit is 1-indexed
            string = self.file_string_array[row_num - 1]
            for col, replacing_char in textColumnMapping.items():
                string = string[:col] + replacing_char + string[col + 1:]
            # update the string array with the new row
            self.file_string_array[row_num - 1] = string
        # create a new text file with the replacement text applied
        self.createOutputFile()

    def find_and_replace_date(self, replacing_date, new_date, rows, position):
        valid_rows = []
        invalid_rows = []
        for row in rows:
            row_string = self.file_string_array[row - 1]
            if row_string[position:position + 8] == replacing_date:
                valid_rows.append(row)
                self.file_string_array[row - 1] = row_string[:position] + new_date + row_string[position + 8:]
            else:
                # the date was not found. With more than 8 errors, return a 'more than 8 errors message'
                invalid_rows.append(row)
        print('hi')
        if len(invalid_rows) > 8:
            return 'Rows {} and more did not contain the date specified.\n' \
                   'Successfully updated {} dates.'.format(invalid_rows[:8], len(valid_rows))
        elif len(invalid_rows) == 0:
            return 'Successfully updated {} dates.'.format(len(valid_rows))
        else:
            return 'Rows {} did not contain the date specified.\n' \
                   'Successfully updated {} dates.'.format(invalid_rows[:8], len(valid_rows))


    # create a map of column numbers to text characters
    # used in the 'replaceText' method
    def mapTextToColumns(self, columns, text):
        mapping = {}
        columns = list(columns)
        columns.sort()
        # map the 0-indexed column number to the character going to replace that column
        for i, c in enumerate(columns):
            # subtract 1 to make the column number 0-indexed
            mapping[c - 1] = text[i]
        return mapping

    # converts the string array back to a text file in the given directory
    def createOutputFile(self):
        # create a processed folder in the working directory if one does not exist
        newpath = self.path + "processed\\"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        # write string array as the new file
        with open('processed\\{}'.format(self.filename), 'w') as filehandle:
            for listitem in self.file_string_array:
                filehandle.write('%s\n' % listitem)

    # creates a directory where all input files should be placed
    def createInputFileDirectory(self):
        self.path = os.getcwd() + "\\"
        # create a files-to-be-processed folder in the working directory if one does not exist
        self.file_input_path = self.path + "files_to_process\\"
        if not os.path.exists(self.file_input_path):
            os.makedirs(self.file_input_path)



