import unittest
from typing import Generator

from tabbyset.testing.test_case import TestCaseAssertions
from tabbyset.entities import TestCase
from tabbyset.__legacy__.file_formats.v1.abc import AbstractTestCasesReader
from io import StringIO


class ReaderForTesting(AbstractTestCasesReader):

    def _parse_as_text(self) -> Generator[TestCase, TestCase, None]:
        csvreader = self._prepare_csv_reader()
        line_number = 0
        for row in csvreader:
            line_number += 1
            if not row:
                continue
            if not row[0]:
                continue
            if 'error' in row[0]:
                raise self._create_reader_exception('Example error', line_number)
            yield TestCase(name=row[0], steps=[])


class TestAbstractReader(TestCaseAssertions, unittest.TestCase):

    def setUp(self):
        self.valid_csv = """
test1
test2
test3
test4
test5
"""
        self.valid_testcases = [
            TestCase(name="test1", steps=[]),
            TestCase(name="test2", steps=[]),
            TestCase(name="test3", steps=[]),
            TestCase(name="test4", steps=[]),
            TestCase(name="test5", steps=[])
        ]

    def test_read_all_returns_all_test_cases(self):
        reader = ReaderForTesting(StringIO(self.valid_csv))
        result = reader.read_all()
        for expected, actual in zip(self.valid_testcases, result):
            self.assertTestCasesEqual(expected, actual)

    def test_after_validity_check_iteration_starts_again(self):
        reader = ReaderForTesting(StringIO(self.valid_csv))
        self.assertTrue(reader.check_validity())
        result = reader.read_all()
        for expected, actual in zip(self.valid_testcases, result):
            self.assertTestCasesEqual(expected, actual)

    def test_iterator(self):
        reader = ReaderForTesting(StringIO(self.valid_csv))
        result = iter(reader)
        for expected, actual in zip(self.valid_testcases, result):
            self.assertTestCasesEqual(expected, actual)

    def test_read_one_returns_first_test_case(self):
        reader = ReaderForTesting(StringIO(self.valid_csv))
        result = reader.read_one()
        self.assertTestCasesEqual(self.valid_testcases[0], result)

    def test_read_one_returns_next_test_case_on_subsequent_calls(self):
        reader = ReaderForTesting(StringIO(self.valid_csv))
        reader.read_one()  # Skip first
        result = reader.read_one()
        self.assertTestCasesEqual(self.valid_testcases[1], result)

    def test_read_one_returns_none_when_no_more_test_cases(self):
        reader = ReaderForTesting(StringIO(self.valid_csv))
        for _ in self.valid_testcases:
            reader.read_one()
        self.assertIsNone(reader.read_one())

    def test_check_validity_returns_true_for_valid_csv(self):
        reader = ReaderForTesting(StringIO(self.valid_csv))
        self.assertTrue(reader.check_validity())

    def test_check_validity_returns_false_for_invalid_csv(self):
        invalid_csv = """
test1
error1
test3
"""
        reader = ReaderForTesting(StringIO(invalid_csv))
        self.assertFalse(reader.check_validity())
