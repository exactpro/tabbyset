from tabbyset.testing import FlexTableAssertions
import tabbyset as tbs

test_multiheader_config = tbs.MultiheaderConfig(row_category_prefix="#category",
                                                column_before_row_category="Category",
                                                header_category_postfix="Categories",
                                                categorizer=lambda row: row.get("Category", 'UNDEFINED'))

tbs.set_default_multiheader_config(test_multiheader_config)
temp_folder = tbs.Folder.mount_from_current_module('__temp__/test_cases_plain_reader')

class TestTestCasesPlainReader(FlexTableAssertions):
    def setUp(self):
        self.test_cases: list[tbs.TestCase] = [
            tbs.TestCase(name="Test 1", steps=[
                { 'Category': 'a', 'A': '1', 'B': '2', 'D': '3', 'Symbol': 'AAPL' },
                { 'Category': 'b', 'B': '4', 'C': '5', 'E': '6', 'Symbol': 'AAPL' },
                { 'Category': 'b', 'B': '1', 'C': '2', 'E': '3', 'Symbol': 'AAPL' },
                { 'Category': 'a', 'A': '4', 'B': '5', 'D': '6', 'Symbol': 'AAPL' }
            ]),
            tbs.TestCase(name="Test 2", steps=[
                { 'Category': 'a', 'A': '1', 'B': '2', 'D': '3', 'Symbol': 'AAPL' },
                { 'Category': 'b', 'B': '4', 'C': '5', 'E': '6', 'Symbol': 'AAPL' },
                { 'Category': 'b', 'B': '1', 'C': '2', 'E': '3', 'Symbol': 'AAPL' },
                { 'Category': 'a', 'A': '4', 'B': '5', 'D': '6', 'Symbol': 'AAPL' }
            ]),
            tbs.TestCase(name="Test 3", steps=[
                { 'Category': 'a', 'A': '1', 'B': '2', 'D': '3', 'Symbol': 'AAPL' },
                { 'Category': 'b', 'B': '4', 'C': '5', 'E': '6', 'Symbol': 'AAPL' },
                { 'Category': 'b', 'B': '1', 'C': '2', 'E': '3', 'Symbol': 'AAPL' },
                { 'Category': 'a', 'A': '4', 'B': '5', 'D': '6', 'Symbol': 'AAPL' }
            ])
        ]
        self.plain_traffic = tbs.FlexTable([
            {'Category': 'a', 'A': '1', 'B': '2', 'D': '3', 'Symbol': 'AAPL'},
            {'Category': 'b', 'B': '4', 'C': '5', 'E': '6', 'Symbol': 'AAPL'},
            {'Category': 'b', 'B': '1', 'C': '2', 'E': '3', 'Symbol': 'AAPL'},
            {'Category': 'a', 'A': '4', 'B': '5', 'D': '6', 'Symbol': 'AAPL'},
            {'Category': 'a', 'A': '1', 'B': '2', 'D': '3', 'Symbol': 'AAPL'},
            {'Category': 'b', 'B': '4', 'C': '5', 'E': '6', 'Symbol': 'AAPL'},
            {'Category': 'b', 'B': '1', 'C': '2', 'E': '3', 'Symbol': 'AAPL'},
            {'Category': 'a', 'A': '4', 'B': '5', 'D': '6', 'Symbol': 'AAPL'},
            {'Category': 'a', 'A': '1', 'B': '2', 'D': '3', 'Symbol': 'AAPL'},
            {'Category': 'b', 'B': '4', 'C': '5', 'E': '6', 'Symbol': 'AAPL'},
            {'Category': 'b', 'B': '1', 'C': '2', 'E': '3', 'Symbol': 'AAPL'},
            {'Category': 'a', 'A': '4', 'B': '5', 'D': '6', 'Symbol': 'AAPL'}
        ])
        with tbs.Csv1Writer(temp_folder.get_file_path('csv1.csv')) as writer:
            writer.write_many(self.test_cases)
        with tbs.Csv2Writer(temp_folder.get_file_path('csv2.csv'),
                            global_columns=tbs.global_columns(self.test_cases)) as writer:
            writer.write_many(self.test_cases)
        with tbs.Csv2Writer(temp_folder.get_file_path('csv2.mhdr.csv'),
                            global_columns=tbs.global_columns(self.test_cases, multiheader=True),
                            multiheader=True) as writer:
            writer.write_many(self.test_cases)

    def enrich_flex_table_rows(self, table: tbs.FlexTable) -> tbs.FlexTable:
        columns = table.columns
        for row in table:
            for column in columns:
                if column not in row:
                    row[column] = ''
        return table

    def test_csv1_plain_reader(self):
        reader = tbs.TestCasesPlainReader(tbs.Csv1Reader(temp_folder.get_file_path('csv1.csv')))
        traffic = tbs.FlexTable(reader)
        self.assertFlexTablesEqual(self.enrich_flex_table_rows(self.plain_traffic), traffic)

    def test_csv2_plain_reader(self):
        reader = tbs.TestCasesPlainReader(tbs.Csv2Reader(temp_folder.get_file_path('csv2.csv')))
        traffic = tbs.FlexTable(reader)
        self.assertFlexTablesEqual(self.enrich_flex_table_rows(self.plain_traffic), traffic)

    def test_csv2_mhdr_plain_reader(self):
        reader = tbs.TestCasesPlainReader(tbs.Csv2Reader(temp_folder.get_file_path('csv2.mhdr.csv'), multiheader=True))
        traffic = tbs.FlexTable(reader)
        self.assertFlexTablesEqual(self.plain_traffic, traffic)

    def test_csv1_headers_exception(self):
        reader = tbs.TestCasesPlainReader(tbs.Csv1Reader(temp_folder.get_file_path('csv1.csv')))
        with self.assertRaises(AttributeError):
            print(reader.headers)

    def test_csv2_headers(self):
        reader = tbs.TestCasesPlainReader(tbs.Csv2Reader(temp_folder.get_file_path('csv2.csv')))
        self.assertEqual(tbs.global_columns(self.test_cases), reader.headers)

    def test_csv2_mhdr_headers(self):
        reader = tbs.TestCasesPlainReader(tbs.Csv2Reader(temp_folder.get_file_path('csv2.mhdr.csv'), multiheader=True))
        self.assertEqual(tbs.global_columns(self.test_cases, multiheader=True), reader.headers)