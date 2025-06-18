import unittest
from pathlib import Path

from tabbyset.file_formats.exceptions import FileParsingException
from tabbyset.testing.test_case import TestCaseAssertions
from tabbyset.entities import TestCase
from tabbyset.file_formats.csv2 import Csv2Reader, Csv2Writer
from tabbyset.file_formats.common.multiheader_csv.config import MultiheaderConfig
from tabbyset.utils import FlexTable, Folder, global_columns
from functools import partial
from tests.test_file_formats.csv2_examples import Csv2Examples
from io import StringIO

temp_folder = Folder.mount_from_current_module('./__temp__')
reader_folder = temp_folder.mount_subfolder('csv2/reader')
writer_folder = temp_folder.mount_subfolder('csv2/writer')

test_multiheader_config = MultiheaderConfig(row_category_prefix="#category",
                                            column_before_row_category="Category",
                                            header_category_postfix="Categories",
                                            categorizer=lambda row: row.get("Category", 'UNDEFINED'))


def get_all_supported_file_formats(csv_example: Csv2Examples):
    stringio = StringIO(csv_example.value)
    csv_file_path = reader_folder.get_file_path(f'{csv_example.name}.csv')
    with open(csv_file_path, 'w', encoding='utf8') as file:
        file.write(csv_example.value)
    return ('textio', stringio), ('csv_file', csv_file_path)


class TestCsv2Reader(TestCaseAssertions, unittest.TestCase):

    def setUp(self):
        Csv2Reader.set_default_multiheader_config(test_multiheader_config)
        self.valid_csv = Csv2Examples.valid.value
        self.valid_testcases = [
            TestCase(
                name="name1",
                steps=FlexTable([
                    {'A': '1', 'B': '2', 'D': '3'},
                    {'A': '4', 'B': '5', 'D': '6'}
                ])
            ),
            TestCase(
                name="name2",
                steps=FlexTable([
                    {'B': '1', 'C': '2', 'E': '3'},
                    {'B': '4', 'C': '5', 'E': '6'}
                ])
            )
        ]
        self.valid_testcases_multiheader = [
            TestCase(
                name="name1",
                steps=FlexTable([
                    {'Category': 'a', 'A': '1', 'B': '2', 'D': '3'},
                    {'Category': 'b', 'B': '4', 'C': '5', 'E': '6'}
                ])
            ),
            TestCase(
                name="name2",
                steps=FlexTable([
                    {'Category': 'b', 'B': '1', 'C': '2', 'E': '3'},
                    {'Category': 'a', 'A': '4', 'B': '5', 'D': '6'}
                ])
            )
        ]

    def test_reading(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid):
            with self.subTest(file_type=t):
                reader = Csv2Reader(content)
                testcases = reader.read_all()
                self.assertEqual(2, len(testcases))
                for expected, actual in zip(self.valid_testcases, testcases):
                    self.assertTestCasesEqual(expected, actual)

    def test_global_columns(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid):
            with self.subTest(file_type=t):
                reader = Csv2Reader(content)
                columns = reader.global_columns
                self.assertEqual(['A', 'B', 'C', 'D', 'E'], columns)


    def test_reading_after_global_columns(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid):
            with self.subTest(file_type=t):
                reader = Csv2Reader(content)
                columns = reader.global_columns
                self.assertEqual(['A', 'B', 'C', 'D', 'E'], columns)
                testcases = reader.read_all()
                self.assertEqual(2, len(testcases))
                for expected, actual in zip(self.valid_testcases, testcases):
                    self.assertTestCasesEqual(expected, actual)

    def test_global_columns_multiheader(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid_multiheader):
            with self.subTest(file_type=t):
                reader = Csv2Reader(content)
                columns = reader.global_columns
                self.assertEqual({
                    'a': ['Category', 'A', 'B', 'D'],
                    'b': ['Category', 'B', 'C', 'E']
                }, columns)

    def test_reading_after_global_columns_multiheader(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid_multiheader):
            with self.subTest(file_type=t):
                reader = Csv2Reader(content)
                columns = reader.global_columns
                self.assertEqual({
                    'a': ['Category', 'A', 'B', 'D'],
                    'b': ['Category', 'B', 'C', 'E']
                }, columns)
                for expected, actual in zip(self.valid_testcases_multiheader, reader):
                    self.assertTestCasesEqual(expected, actual)
                reader.close()

    def test_no_header(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.invalid_no_header):
            with self.subTest(file_type=t):
                reader = Csv2Reader(content)
                self.assertFalse(reader.check_validity())
                with self.assertRaises(FileParsingException):
                    print(reader.read_all())
                reader.close()

    def test_double_start(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.invalid_double_start):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv2Reader(content).read_all())

    def test_double_end(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.invalid_double_end):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv2Reader(content).read_all())

    def test_nameless(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.invalid_no_name):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv2Reader(content).read_all())

    def test_header_single_element(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.invalid_header_single_element):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv2Reader(content).read_all())

    def test_extra_case_column(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.invalid_extra_case_column):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv2Reader(content).read_all())

    def test_extra_empty_case_column(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid_extra_empty_case_column):
            with self.subTest(file_type=t):
                self.assertTestCasesEqual(self.valid_testcases[0], Csv2Reader(content).read_one())

    def test_less_case_columns_than_global_columns(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid_less_case_columns_than_global_columns):
            with self.subTest(file_type=t):
                self.valid_testcases[0].steps.remove_column('D')
                self.assertTestCasesEqual(self.valid_testcases[0], Csv2Reader(content).read_one())

    def test_extra_empty_values(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid_extra_empty_values):
            with self.subTest(file_type=t):
                for expected, actual in zip(self.valid_testcases, Csv2Reader(content).read_all()):
                    self.assertTestCasesEqual(expected, actual)

    def test_not_enough_values(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid_not_enough_values):
            with self.subTest(file_type=t):
                self.valid_testcases[0].steps[0]['D'] = ''
                for expected, actual in zip(self.valid_testcases, Csv2Reader(content).read_all()):
                    self.assertTestCasesEqual(expected, actual)

    def test_case_not_closed(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.invalid_test_case_not_closed):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv2Reader(content).read_all())

    def test_no_table(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid_no_table):
            with self.subTest(file_type=t):
                self.valid_testcases[0].set_steps([])
                self.assertTestCasesEqual(self.valid_testcases[0], Csv2Reader(content).read_one())

    def test_nameless_column(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid_nameless_column):
            with self.subTest(file_type=t):
                self.valid_testcases[0].steps.remove_column('D')
                self.assertTestCasesEqual(self.valid_testcases[0], Csv2Reader(content).read_one())

    def test_valid_multiheader(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid_multiheader):
            with self.subTest(file_type=t):
                with Csv2Reader(content, multiheader=True) as csv2_reader:
                    for expected, actual in zip(self.valid_testcases_multiheader, csv2_reader):
                        self.assertTestCasesEqual(expected, actual)

    def test_multiheader_too_much_values(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid_multiheader_too_much_values):
            with self.subTest(file_type=t):
                with Csv2Reader(content, multiheader=True) as csv2_reader:
                    for expected, actual in zip(self.valid_testcases_multiheader, csv2_reader):
                        self.assertTestCasesEqual(expected, actual)

    def test_multiheader_less_values(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.valid_multiheader_less_values):
            with self.subTest(file_type=t):
                self.valid_testcases_multiheader[0].steps[0]['D'] = ''
                self.valid_testcases_multiheader[0].steps[1]['E'] = ''
                with Csv2Reader(content, multiheader=True) as csv2_reader:
                    for expected, actual in zip(self.valid_testcases_multiheader, csv2_reader):
                        self.assertTestCasesEqual(expected, actual)

    def test_multiheader_empty_category_value(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.invalid_multiheader_empty_category_value):
            with self.subTest(file_type=t):
                with Csv2Reader(content, multiheader=True) as csv2_reader:
                    with self.assertRaises(FileParsingException):
                        print(list(csv2_reader))

    def test_multiheader_misleading_category_value(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.invalid_multiheader_misleading_category_value):
            with self.subTest(file_type=t):
                with Csv2Reader(content, multiheader=True) as csv2_reader:
                    with self.assertRaises(FileParsingException):
                        print(list(csv2_reader))

    def test_multiheader_undefined_category(self):
        for t, content in get_all_supported_file_formats(Csv2Examples.invalid_multiheader_undefined_category):
            with self.subTest(file_type=t):
                with Csv2Reader(content, multiheader=True) as csv2_reader:
                    with self.assertRaises(FileParsingException):
                        print(list(csv2_reader))


class TestCsv2Writer(TestCaseAssertions, unittest.TestCase):
    def setUp(self):
        Csv2Writer.set_default_multiheader_config(test_multiheader_config)
        self.valid_csv = """
A,B,C,D,E\r
TEST_CASE_START,name1,,,\r
A,B,,D,\r
1,2,,3,\r
4,5,,6,\r
TEST_CASE_END,,,,\r
TEST_CASE_START,name2,,,\r
,B,C,,E\r
,1,2,,3\r
,4,5,,6\r
TEST_CASE_END,,,,\r
"""
        self.global_columns = ['A', 'B', 'C', 'D', 'E']
        self.valid_testcases = [
            TestCase(
                name="name1",
                steps=FlexTable([
                    {'A': '1', 'B': '2', 'D': '3'},
                    {'A': '4', 'B': '5', 'D': '6'}
                ])
            ),
            TestCase(
                name="name2",
                steps=FlexTable([
                    {'B': '1', 'C': '2', 'E': '3'},
                    {'B': '4', 'C': '5', 'E': '6'}
                ])
            )
        ]

    def test_writing_stringio(self):
        content = StringIO()
        writer = Csv2Writer(content, self.global_columns)
        writer.write(self.valid_testcases[0])
        writer.write(self.valid_testcases[1])
        self.assertEqual(self.valid_csv.strip(), content.getvalue().strip())

    def test_writing_file_path(self):
        folder = Folder.mount_from_current_module('../assets/csv2')
        filepath = folder.get_file_path('valid.matrix.csv')
        writer = Csv2Writer(filepath, self.global_columns)
        for testcase in self.valid_testcases:
            writer.write(testcase)
        writer.close()
        with open(filepath, 'r', newline='', encoding='utf8') as file:
            self.assertEqual(self.valid_csv.strip(), file.read().strip())
        folder.clear()


class TestCsv2ReadWrite(TestCaseAssertions):

    def test_data_is_not_changed_during_read_write(self):
        Csv2Writer.set_default_multiheader_config(test_multiheader_config)
        Csv2Reader.set_default_multiheader_config(test_multiheader_config)
        custom_global_columns = partial(global_columns, categorizer=test_multiheader_config.categorizer)
        for csv_example in Csv2Examples:
            if csv_example.name.startswith('invalid'):
                continue
            with self.subTest(example=csv_example.name):
                for t, content in get_all_supported_file_formats(csv_example):
                    with self.subTest(file_type=t):
                        reader = Csv2Reader(content)
                        first_reading_testcases = reader.read_all()
                        reader.close()
                        if t == 'textio':
                            new_content = StringIO()
                        elif t == 'csv_file':
                            new_content = writer_folder.get_file_path(Path(content).name)
                        is_multiheader = 'multiheader' in csv_example.name
                        columns_to_provide = custom_global_columns(first_reading_testcases, multiheader=is_multiheader)
                        if not is_multiheader and not any(columns_to_provide):
                            columns_to_provide = ['A', 'B', 'C', 'D', 'E']
                        writer = Csv2Writer(new_content, columns_to_provide)
                        for testcase in first_reading_testcases:
                            writer.write(testcase)
                        if t == 'textio':
                            new_content.seek(0)
                        if t == 'csv_file':
                            writer.close()
                        second_reading_testcases = Csv2Reader(new_content).read_all()
                        self.assertEqual(len(first_reading_testcases), len(second_reading_testcases))
                        for first, second in zip(first_reading_testcases, second_reading_testcases):
                            self.assertTestCasesEqual(first, second)


if __name__ == '__main__':
    unittest.main()
