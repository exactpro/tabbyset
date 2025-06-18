from io import StringIO

import tabbyset as tbs
from unittest import TestCase

test_multiheader_config = tbs.MultiheaderConfig(row_category_prefix="#category",
                                            column_before_row_category="Category",
                                            header_category_postfix="Categories",
                                            categorizer=lambda row: row.get("Category", 'UNDEFINED'))

mhdr_csv_example = """
Category,#category:a,A,B,D,HeaderDefinition,HeaderDefinitionCategories:a
Category,#category:b,B,C,E,HeaderDefinition,HeaderDefinitionCategories:b
a,#category:a,1,2,3
b,#category:b,4,5,6
b,#category:b,1,2,3
a,#category:a,4,5,6
"""

expected_headers = {
    'a': ['Category', 'A', 'B', 'D'],
    'b': ['Category', 'B', 'C', 'E']
}

expected_rows = [
    { 'Category': 'a', 'A': '1', 'B': '2', 'D': '3' },
    { 'Category': 'b', 'B': '4', 'C': '5', 'E': '6' },
    { 'Category': 'b', 'B': '1', 'C': '2', 'E': '3' },
    { 'Category': 'a', 'A': '4', 'B': '5', 'D': '6' }
]

class TestMultiheaderCsv(TestCase):
    def setUp(self):
        self.reading_stream = StringIO(mhdr_csv_example)

    def test_read_content(self):
        reader = tbs.MHdrCsvReader(self.reading_stream, multiheader_config=test_multiheader_config)
        rows = list(reader)
        self.assertEqual(rows, expected_rows)

    def test_read_headers(self):
        reader = tbs.MHdrCsvReader(self.reading_stream, multiheader_config=test_multiheader_config)
        self.assertEqual(expected_headers, reader.headers)

    def test_read_headers_and_content(self):
        reader = tbs.MHdrCsvReader(self.reading_stream, multiheader_config=test_multiheader_config)
        headers = reader.headers
        rows = list(reader)
        self.assertEqual(expected_headers, headers)
        self.assertEqual(expected_rows, rows)

    def test_write_read_content(self):
        write_stream = StringIO()
        writer = tbs.MHdrCsvWriter(write_stream, headers=expected_headers, multiheader_config=test_multiheader_config)
        writer.writeheaders()
        writer.writerows(expected_rows)
        write_stream.seek(0)
        reader = tbs.MHdrCsvReader(write_stream, multiheader_config=test_multiheader_config)
        headers = reader.headers
        rows = list(reader)
        self.assertEqual(expected_headers, headers)
        self.assertEqual(expected_rows, rows)
