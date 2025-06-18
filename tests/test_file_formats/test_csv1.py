import unittest
from pathlib import Path
from string import Template

import tabbyset as tbs
from tabbyset.file_formats.exceptions import FileParsingException
from tabbyset.testing.test_case import TestCaseAssertions
from tabbyset.entities import TestCase
from tabbyset.file_formats.csv1 import Csv1Reader, Csv1Writer
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
                {'A': '1', 'B': '2', 'C': '3'},
                {'A': '4', 'B': '5', 'C': '6'}
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

    def test_valid_id(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.valid_new_id):
            with self.subTest(file_type=t):
                with Csv1Reader(content) as reader:
                    tc_read = reader.read_one()
                    self.assertEqual(tc_read.id, '2e9b7b8c-2d9f-4f65-858a-1bb339885e23',
                                     'Reader must keep valid UUID')
                    self.assertTestCasesEqual(tc_read, self.valid_testcase)

    def test_invalid_id(self):
        for t, content in get_all_supported_file_formats(Csv1Examples.valid):
            with self.subTest(file_type=t):
                with Csv1Reader(content) as reader:
                    tc_read = reader.read_one()
                    self.assertTestCasesEqual(tc_read, self.valid_testcase)
                    generated_id = tbs.TestsTracker.get_id_from_steps(self.valid_testcase)
                    self.assertEqual(tc_read.id, generated_id,
                                     'Reader must replace invalid UUID with UUIDv5 generated from steps')

    def test_no_instrument(self):
        self.skipTest('This is a legacy requirement')
        for t, content in get_all_supported_file_formats(Csv1Examples.invalid_no_instrument):
            with self.subTest(file_type=t):
                with self.assertRaises(FileParsingException):
                    print(Csv1Reader(content).read_all())

    def test_instrument_only_in_rows(self):
        self.skipTest('This is a legacy requirement')
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
        test_case_id = tbs.TestsTracker.new_id()
        self.valid_testcase = TestCase(
            name="name",
            description="description",
            steps=FlexTable([
                {'A': '1', 'B': '2', 'C': '3'},
                {'A': '4', 'B': '5', 'C': '6'}
            ]),
            id=test_case_id
        )
        self.valid_csv_template = Template("""
TEST_CASE_START\r
name\r
$id\r
description\r
A,B,C\r
1,2,3\r
4,5,6\r
TEST_CASE_END\r
""")
        self.valid_csv = self.valid_csv_template.substitute(id=test_case_id)

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
        valid_csv = f"""
TEST_CASE_START\r
name\r
{self.valid_testcase.id}\r
description\r
B,A,C\r
2,1,3\r
5,4,6\r
TEST_CASE_END\r
"""
        self.assertEqual(valid_csv.strip(), content.getvalue().strip())

    def test_write_invalid_id(self):
        self.valid_testcase.id = 'invalid'
        generated_id = tbs.TestsTracker.get_id_from_steps(self.valid_testcase)
        content = StringIO()
        writer = Csv1Writer(content)
        writer.write(self.valid_testcase)
        content.seek(0)
        reader = Csv1Reader(content)
        test_case = reader.read_one()
        self.assertNotEqual(test_case.id, generated_id, 'Writer must generate UUIDv4, not UUIDv5')
        self.assertTrue(tbs.TestsTracker.is_valid_id(test_case.id), 'Writer must keep valid UUID')

    def test_write_valid_id(self):
        content = StringIO()
        writer = Csv1Writer(content)
        writer.write(self.valid_testcase)
        content.seek(0)
        reader = Csv1Reader(content)
        test_case = reader.read_one()
        self.assertEqual(test_case.id, self.valid_testcase.id, 'Writer must keep valid UUID')


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
