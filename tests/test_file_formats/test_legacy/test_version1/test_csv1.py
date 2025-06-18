import unittest
from pathlib import Path

from tabbyset.file_formats.exceptions import FileParsingException
from tabbyset.testing.test_case import TestCaseAssertions
from tabbyset.entities import TestCase
from tabbyset.__legacy__.file_formats.v1.csv1 import Csv1Reader, Csv1Writer
from tabbyset.utils import FlexTable, Folder
from tests.test_file_formats.csv1_examples import Csv1Examples
from io import StringIO

temp_folder = Folder.mount_from_current_module('./__temp__')
reader_folder = temp_folder.mount_subfolder('csv1/reader')
writer_folder = temp_folder.mount_subfolder('csv1/writer')


def get_all_supported_file_formats(csv_example: Csv1Examples):
    stringio = StringIO(csv_example.value)
    csv_file_path = reader_folder.get_file_path(f'{csv_example.name}.csv')
    with open(csv_file_path, 'w', encoding='utf8') as file:
        file.write(csv_example.value)
    return ('textio', stringio), ('csv_file', csv_file_path)


class TestCsv1Reader(TestCaseAssertions, unittest.TestCase):

    def setUp(self):
        self.valid_csv = Csv1Examples.valid.value
        self.valid_testcase = TestCase(
            name="name",
            description="description",
            steps=FlexTable([
                {'A': '1', 'B': '2', 'C': '3', 'Symbol': 'instrument'},
                {'A': '4', 'B': '5', 'C': '6', 'Symbol': 'instrument'}
            ])
        )

    def test_reading(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.valid):
            with self.subTest(file_type=t):
                reader = Csv1Reader(content)
                testcases = reader.read_all()
                self.assertEqual(1, len(testcases))
                testcase = testcases[0]
                self.assertTestCasesEqual(self.valid_testcase, testcase)

    def test_double_start(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.invalid_double_start):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv1Reader(content).read_all())

    def test_double_end(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.invalid_double_end):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv1Reader(content).read_all())

    def test_nameless(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.invalid_no_name):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv1Reader(content).read_all())

    def test_no_instrument(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.invalid_no_instrument):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv1Reader(content).read_all())

    def test_instrument_only_in_rows(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.valid_instrument_only_in_rows):
            with self.subTest(file_type=t):
                self.assertTestCasesEqual(Csv1Reader(content).read_one(), self.valid_testcase)

    def test_no_description(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.valid_no_description):
            with self.subTest(file_type=t):
                self.valid_testcase.description = ''
                self.assertTestCasesEqual(Csv1Reader(content).read_one(), self.valid_testcase)

    def test_extra_empty_values(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.valid_extra_empty_values):
            with self.subTest(file_type=t):
                self.assertTestCasesEqual(Csv1Reader(content).read_one(), self.valid_testcase)

    def test_not_enough_values(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.valid_not_enough_values):
            with self.subTest(file_type=t):
                self.valid_testcase.steps[0]['C'] = ''
                self.assertTestCasesEqual(Csv1Reader(content).read_one(), self.valid_testcase)

    def test_case_not_closed(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.invalid_test_case_not_closed):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv1Reader(content).read_all())

    def test_no_table(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.valid_no_table):
            with self.subTest(file_type=t):
                self.valid_testcase.set_steps([])
                self.assertTestCasesEqual(Csv1Reader(content).read_one(), self.valid_testcase)

    def test_nameless_column(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.valid_nameless_column):
            with self.subTest(file_type=t):
                self.valid_testcase.steps.remove_column('C')
                self.assertTestCasesEqual(Csv1Reader(content).read_one(), self.valid_testcase)


class TestCsv1Writer(TestCaseAssertions, unittest.TestCase):
    def setUp(self):
        self.valid_csv = """
TEST_CASE_START\r
name\r
instrument\r
description\r
Symbol,A,B,C\r
instrument,1,2,3\r
instrument,4,5,6\r
TEST_CASE_END\r
"""
        self.valid_testcase = TestCase(
            name="name",
            description="description",
            steps=FlexTable([
                {'A': '1', 'B': '2', 'C': '3', 'Symbol': 'instrument'},
                {'A': '4', 'B': '5', 'C': '6', 'Symbol': 'instrument'}
            ])
        )

    def test_writing_stringio(self):
        content = StringIO()
        writer = Csv1Writer(content)
        writer.write(self.valid_testcase)
        self.assertEqual(self.valid_csv.strip(), content.getvalue().strip())

    def test_writing_file_path(self):
        folder = Folder.mount_from_current_module('./__temp__/csv1/writer')
        filepath = folder.get_file_path('valid.csv')
        writer = Csv1Writer(filepath)
        writer.write(self.valid_testcase)
        writer.close()
        with open(filepath, 'r', newline='', encoding='utf8') as file:
            self.assertEqual(self.valid_csv.strip(), file.read().strip())
        folder.clear()

    def test_custom_columns_order(self):
        content = StringIO()
        writer = Csv1Writer(content, first_priority_columns=['B', 'A'], last_priority_columns=['C'])
        writer.write(self.valid_testcase)
        valid_csv = """
TEST_CASE_START\r
name\r
instrument\r
description\r
B,A,Symbol,C\r
2,1,instrument,3\r
5,4,instrument,6\r
TEST_CASE_END\r
"""
        self.assertEqual(valid_csv.strip(), content.getvalue().strip())


class TestCsv1ReadWrite(TestCaseAssertions):

    def test_data_is_not_changed_during_read_write(self):
        for csv_example in Csv1Examples:
            if csv_example.name.startswith('invalid'):
                continue
            with self.subTest(example=csv_example.name):
                for t, content in get_all_supported_file_formats(csv_example):
                    with self.subTest(file_type=t):
                        reader = Csv1Reader(content)
                        first_reading_testcases = reader.read_all()
                        reader.close()
                        if t == 'textio':
                            new_content = StringIO()
                        elif t == 'csv_file':
                            new_content = writer_folder.get_file_path(Path(content).name)
                        writer = Csv1Writer(new_content)
                        for testcase in first_reading_testcases:
                            writer.write(testcase)
                        if t == 'textio':
                            new_content.seek(0)
                        if t == 'csv_file':
                            writer.close()
                        second_reading_testcases = Csv1Reader(new_content).read_all()
                        self.assertEqual(len(first_reading_testcases), len(second_reading_testcases))
                        for first, second in zip(first_reading_testcases, second_reading_testcases):
                            self.assertTestCasesEqual(first, second)


if __name__ == '__main__':
    unittest.main()
