import tabbyset as tbs
from tabbyset.testing import TestCaseAssertions


class TestGroupBy(TestCaseAssertions):

    empty_table = tbs.FlexTable([])
    table_as_list = [{'Action': "Send", 'Protocol': "FIX"},
                    {'Action': "Receive", 'Protocol': "OUTCH"},
                    {'Action': "Send", 'Protocol': "SAIL"},
                    {'Action': "Send", 'Protocol': "SAIL"}]
    table_by_default = tbs.FlexTable(table_as_list)
    expected_result_grouped_by_action = {('Receive',): [{'Action': 'Receive', 'Protocol': 'OUTCH'}],
                                        ('Send',): [{'Action': 'Send', 'Protocol': 'FIX'},
                                                    {'Action': 'Send', 'Protocol': 'SAIL'},
                                                    {'Action': 'Send', 'Protocol': 'SAIL'}]}

    def test_group_by_single_column(self):
        result = tbs.group_by(self.table_by_default, ['Action'])

        self.assertEqual(result, self.expected_result_grouped_by_action)
        self.assertEqual(len(result[('Receive',)]), 1)
        self.assertEqual(len(result[("Send",)]), 3)

    def test_group_by_multiple_columns(self):
        result = tbs.group_by(self.table_by_default, ['Action', 'Protocol'])
        expected_result = {('Receive', 'OUTCH'): [{'Action': 'Receive', 'Protocol': 'OUTCH'}],
                            ('Send', 'FIX'): [{'Action': 'Send', 'Protocol': 'FIX'}],
                            ('Send', 'SAIL'): [{'Action': 'Send', 'Protocol': 'SAIL'},{'Action': 'Send', 'Protocol': 'SAIL'}]}
        self.assertEqual(set(result.keys()), {('Send', 'FIX'), ('Send', 'SAIL'), ('Receive', 'OUTCH')})
        self.assertEqual(result, expected_result)
        self.assertEqual(len(result[('Receive', 'OUTCH')]), 1)
        self.assertEqual(result[('Send', 'FIX')], [{'Action': 'Send', 'Protocol': 'FIX'}])
        self.assertEqual(len(result[('Send', 'FIX')]), 1)

    def test_group_by_empty_table(self):
        result = tbs.group_by(self.empty_table, ['Action'])
        self.assertEqual(result, {})

    def test_group_by_no_columns(self):
        result = tbs.group_by(self.table_by_default, [])
        # All rows should be grouped together under the empty tuple key
        self.assertEqual(set(result.keys()), {()})
        self.assertEqual(len(result[()]), 4)

    def test_group_by_invalid_columns_type(self):
        with self.assertRaises(TypeError):
            tbs.group_by(self.table_by_default, None)

    def test_group_by_string_columns_type(self):
        result = tbs.group_by(self.table_by_default, 'Action')
        self.assertEqual(result, self.expected_result_grouped_by_action)

    def test_group_by_missing_column(self):
        # Should group by None for missing column
        result = tbs.group_by(self.table_by_default, ['Action', 'User'])
        self.assertEqual(result.keys(), {('Send', None), ('Receive', None)})

    def test_group_by_table_as_list(self):
        result = tbs.group_by(self.table_as_list, ['Action'])
        self.assertEqual(result.keys(), {('Send', ), ('Receive', )})

    def test_group_by_with_count(self):
        result = tbs.group_by(self.table_by_default, ['Action'], count=True)
        self.assertEqual(result[('Send', )], 3)
        self.assertEqual(result[('Receive', )], 1)

    def test_group_by_with_invalid_table(self):
        with self.assertRaises(TypeError):
            tbs.group_by({1, 2, 3}, ['Action'])

    def test_group_by_with_invalid_table_instances(self):
        with self.assertRaises(TypeError):
            tbs.group_by((None, None, None), ['Action'])



