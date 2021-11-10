import unittest
from unittest import TestCase
from EditorMenu import EditorMenu


class TestEditor(unittest.TestCase):
    def setUp(self):
        self.editor = EditorMenu()
#
class TestMenuInput(TestEditor):
    def test_process_user_col_row_positions(self):
        output = set()
        positions = '1, 3-4, 5, 6, 7'
        errors = self.editor.process_user_col_row_positions(positions, output)
        self.assertEqual(output, {1, 3, 4, 5, 6, 7})
        self.assertEqual(errors, [])

    def test_process_user_col_row_positions_2(self):
        output = set()
        positions = '1-7, 8, 10, 12-13'
        errors = self.editor.process_user_col_row_positions(positions, output)
        self.assertEqual(output, {1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 13})
        self.assertEqual(errors, [])

    def test_process_user_col_row_positions_3(self):
        output = set()
        positions = 'eight, 1, 3, two, 9, 10-14'
        errors = self.editor.process_user_col_row_positions(positions, output)
        self.assertEqual(output, {1, 3, 9, 10, 11, 12, 13, 14})
        self.assertEqual(errors, ['eight', 'two'])

    def test_process_user_col_row_positions_4(self):
        output = set()
        positions = '1-3, 5-6, 9-16'
        errors = self.editor.process_user_col_row_positions(positions, output)
        self.assertEqual(output, {1, 2, 3, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16})
        self.assertEqual(errors, [])

    def test_handle_user_col_row_input_errors(self):
        pass

    def test_handle_user_text_length_error(self):
        pass

