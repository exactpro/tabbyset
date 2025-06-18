import random

import tabbyset as tbs
from tabbyset.testing.test_case import TestCaseAssertions

reader_folder = tbs.Folder.mount_from_current_module('./__temp__').mount_subfolder('tcs_jsonl/reader')
writer_folder = tbs.Folder.mount_from_current_module('./__temp__').mount_subfolder('tcs_jsonl/writer')

class TestTcsJsonl(TestCaseAssertions):
    def setUp(self):
        possible_columns = ["A", "B", "C", "D", "E", "F"]
        possible_values = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "FB", *range(1, 11), ""]
        self.test_cases = [
            tbs.TestCase(f"Test Case {i}", [
                {
                    column: random.choice(possible_values)
                    for column in random.choices(possible_columns, k=random.randint(1, 6))
                } for _ in range(random.randint(1, 10))
            ]) for i in range(10)
        ]

    def test_write_read(self):
        with self.subTest('writing'):
            with tbs.RawTestCasesWriter(writer_folder.get_file_path("tests.jsonl")) as writer:
                writer.write_many(self.test_cases)
        with self.subTest('reading'):
            with tbs.RawTestCasesReader(writer_folder.get_file_path("tests.jsonl")) as reader:
                for expected, actual in zip(self.test_cases, reader.read_all()):
                    with self.subTest(test_case=expected.name):
                        self.assertTestCasesEqual(expected, actual)
