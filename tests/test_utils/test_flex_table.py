import unittest
from tabbyset.testing import TestCaseAssertions
from tabbyset.utils.flex_table import FlexTable, ascii_table
from tabbyset.testing.diff import ColoredString, ConsoleColor


class TestFlexTable(TestCaseAssertions):

    def setUp(self):
        self.non_empty_flex_table = FlexTable([{'col1': 'value1', 'col2': 2}])
        self.big_table = FlexTable()
        for i in range(1000):
            self.big_table.append({'col1': f'value{i}', 'col2': i})

    def test_initialization(self):
        flex_table = FlexTable()
        self.assertEqual(len(flex_table), 0)
        self.assertEqual(flex_table.columns, [])

    def test_append_row(self):
        flex_table = FlexTable()
        flex_table.append({'col1': 'value1', 'col2': 2})
        self.assertEqual(len(flex_table), 1)
        self.assertIn('col1', flex_table.columns)
        self.assertIn('col2', flex_table.columns)

    def test_extend_rows(self):
        flex_table = FlexTable()
        rows = [{'col1': 'value1'}, {'col2': 2}]
        flex_table.extend(rows)
        self.assertEqual(len(flex_table), 2)
        self.assertIn('col1', flex_table.columns)
        self.assertIn('col2', flex_table.columns)

    def test_setitem_positive(self):
        self.non_empty_flex_table[0] = {}
        self.non_empty_flex_table['col11'] = ['value11']
        self.assertEqual(len(self.non_empty_flex_table), 1)
        self.assertNotIn('col1', self.non_empty_flex_table.columns)
        self.assertIn('col11', self.non_empty_flex_table.columns)

    def test_setitem_negative(self):
        self.assertRaises(TypeError, self.non_empty_flex_table.__setitem__, {}, 0)

    def test_getitem(self):
        self.assertEqual(self.non_empty_flex_table[0], {'col1': 'value1', 'col2': 2})
        self.assertFlexTablesEqual(self.non_empty_flex_table[:1], FlexTable([{'col1': 'value1', 'col2': 2}]))
        self.assertEqual(self.non_empty_flex_table['col1'], ['value1'])

    def test_getitem_query(self):
        result = self.big_table[{'col2': '> 500', 'col1': '<= value700'}]
        self.assertEqual(len(result), 200)
        for row in result:
            self.assertGreater(row['col2'], 500)
            self.assertLessEqual(row['col1'], 'value700')

    def test_getitem_invalid_index(self):
        flex_table = FlexTable()
        with self.assertRaises(TypeError):
            _ = flex_table[1.11]

    def test_remove_column(self):
        self.non_empty_flex_table.remove_column('col1')
        self.assertNotIn('col1', self.non_empty_flex_table.columns)
        self.assertIn('col2', self.non_empty_flex_table.columns)

    def test_delitem(self):
        del self.non_empty_flex_table[0]
        self.assertEqual(len(self.non_empty_flex_table), 0)

    def test_delitem_column(self):
        del self.non_empty_flex_table['col1']
        self.assertNotIn('col1', self.non_empty_flex_table.columns)
        self.assertIn('col2', self.non_empty_flex_table.columns)

    def test_contains(self):
        self.assertIn({'col1': 'value1', 'col2': 2}, self.non_empty_flex_table)
        self.assertNotIn({'col1': 'value2', 'col2': 3}, self.non_empty_flex_table)
        self.assertIn({'col1': 'value1'}, self.non_empty_flex_table)
        self.assertNotIn({'col1': '> value2'}, self.non_empty_flex_table)
        self.assertIn({'col1': '< value2'}, self.non_empty_flex_table)
        self.assertIn({'col2': '> 1'}, self.non_empty_flex_table)

    def test_count(self):
        table = FlexTable([{'Action': 'Quote'}, {'Action': 'Trade'}, {'Action': 'Quote'}])
        self.assertEqual(table.count({'Action': 'Quote'}), 2)
        self.assertEqual(table.count({'Action': 'Trade'}), 1)
        self.assertEqual(table.count({'Action': 'Nonexistent'}), 0)

    def test_index(self):
        table = FlexTable([{'Action': 'Quote'}, {'Action': 'Trade'}, {'Action': 'Quote'}])
        self.assertEqual(table.index({'Action': 'Quote'}), 0)
        self.assertEqual(table.index({'Action': 'Trade'}), 1)
        with self.assertRaises(ValueError):
            table.index({'Action': 'Nonexistent'})

    def test_pop(self):
        table = FlexTable([{'Action': 'Quote'}, {'Action': 'Trade'}, {'Action': 'Quote'}])
        self.assertEqual(table.pop(1), {'Action': 'Trade'})
        self.assertEqual(len(table), 2)
        self.assertEqual(table.pop(), {'Action': 'Quote'})
        self.assertEqual(len(table), 1)

    def test_remove(self):
        table = FlexTable([{'Action': 'Quote'}, {'Action': 'Trade'}, {'Action': 'Quote'}])
        table.remove({'Action': 'Quote'})
        self.assertEqual(len(table), 1)
        self.assertEqual(table[0], {'Action': 'Trade'})

    def test_clear(self):
        table = FlexTable([{'Action': 'Quote'}, {'Action': 'Trade'}, {'Action': 'Quote'}])
        table.clear()
        self.assertEqual(len(table), 0)

    def test_sort(self):
        with self.subTest('Sort empty table'):
            table = FlexTable([])
            sorted_table = table.sort()
            self.assertEqual(sorted_table.rows, [])

        with self.subTest('Sort single row table'):
            table = FlexTable([{'Action': 'Quote'}])
            sorted_table = table.sort()
            self.assertEqual(sorted_table.rows, [{'Action': 'Quote'}])

        with self.subTest('Sort multiple rows table'):
            table = FlexTable([{'Action': 'Trade'}, {'Action': 'Quote'}, {'Action': 'Quote'}])
            sorted_table = table.sort(key=lambda row: row['Action'])
            self.assertEqual(sorted_table.rows, [{'Action': 'Quote'}, {'Action': 'Quote'}, {'Action': 'Trade'}])

        with self.subTest('Sort multiple rows table reverse'):
            table = FlexTable([{'Action': 'Trade'}, {'Action': 'Quote'}, {'Action': 'Quote'}])
            sorted_table = table.sort(key=lambda row: row['Action'], reverse=True)
            self.assertEqual(sorted_table.rows, [{'Action': 'Trade'}, {'Action': 'Quote'}, {'Action': 'Quote'}])

    def test_reverse(self):
        with self.subTest('Reverse empty table'):
            table = FlexTable([])
            reversed_table = table.reverse()
            self.assertEqual(reversed_table.rows, [])

        with self.subTest('Reverse single row table'):
            table = FlexTable([{'Action': 'Quote'}])
            reversed_table = table.reverse()
            self.assertEqual(reversed_table.rows, [{'Action': 'Quote'}])

        with self.subTest('Reverse multiple rows table'):
            table = FlexTable([{'Action': 'Quote'}, {'Action': 'Trade'}, {'Action': 'Quote'}])
            reversed_table = table.reverse()
            self.assertEqual(reversed_table.rows, [{'Action': 'Quote'}, {'Action': 'Trade'}, {'Action': 'Quote'}][::-1])

    def test_equality(self):
        table1 = FlexTable()
        table2 = FlexTable()
        table1.append({'col1': 'value1'})
        table2.append({'col1': 'value1'})
        self.assertEqual(table1, table2)

    def test_inequality(self):
        table1 = FlexTable()
        table2 = FlexTable()
        table1.append({'col1': 'value1'})
        table2.append({'col2': 'value2'})
        self.assertNotEqual(table1, table2)
        self.assertNotEqual(table1, 'table1')

    def test_repr(self):
        expected_repr = "FlexTable([{'col1': 'value1', 'col2': 2}])"
        self.assertEqual(repr(self.non_empty_flex_table), expected_repr)

    def test_as_ascii_table(self):
        expected_str = "col1   | col2\n=======|======\nvalue1 | 2   "
        self.assertEqual(self.non_empty_flex_table.as_ascii_table(), expected_str)

    def test_copy(self):
        table_copy = self.non_empty_flex_table.copy()
        self.assertEqual(self.non_empty_flex_table, table_copy)
        self.assertIsNot(self.non_empty_flex_table, table_copy)

    def test_add(self):
        table1 = FlexTable([{'col1': 'value1', 'col2': 2}])
        expected_table = FlexTable([{'col1': 'value1', 'col2': 2}, {'col1': 'value2', 'col2': 3}])
        with self.subTest('Add FlexTable'):
            table2 = FlexTable([{'col1': 'value2', 'col2': 3}])
            self.assertEqual(table1 + table2, expected_table)
        with self.subTest('Add dict'):
            self.assertEqual(table1 + {'col1': 'value2', 'col2': 3}, expected_table)
        with self.subTest('Add list'):
            self.assertEqual(table1 + [{'col1': 'value2', 'col2': 3}], expected_table)

    def test_iadd(self):
        table1 = FlexTable([{'col1': 'value1', 'col2': 2}])
        table1 += {'col1': 'value2', 'col2': 3}
        self.assertEqual(table1, FlexTable([{'col1': 'value1', 'col2': 2}, {'col1': 'value2', 'col2': 3}]))

    def test_hash(self):
        original_table = self.big_table
        with self.subTest('Same table'):
            self.assertEqual(hash(original_table), hash(original_table))
        with self.subTest('Same table with meaningless column'):
            table_with_meaningless_column = self.big_table.copy(deep=True)
            table_with_meaningless_column['meaningless'] = ''
            self.assertEqual(hash(original_table), hash(table_with_meaningless_column))
        with self.subTest('Same table with different columns order'):
            table_with_swapped_columns = self.big_table.copy(deep=True)
            table_with_swapped_columns[0] = {'col2': 0, 'col1': 'value0'}
            self.assertEqual(hash(original_table), hash(table_with_swapped_columns))
        with self.subTest('Different table'):
            self.assertNotEqual(hash(original_table), hash(self.non_empty_flex_table))


class TestAsciiTable(unittest.TestCase):
    def test_ascii_table(self):
        table = ascii_table([
            ['col1', 'col2'],
            ['value1', 2]
        ])
        expected_table = "col1   | col2\n=======|======\nvalue1 | 2   "
        self.assertEqual(table, expected_table)

    def test_ascii_table_colored(self):
        ref_width = [
            [4, 4],
            [6, 1]
        ]
        table = ascii_table([
            ['col1', ColoredString('col2', ConsoleColor.CYAN)],
            [ColoredString('value1', ConsoleColor.RED), 2]
        ], ref_width)
        expected_table = "col1   | \x1b[36mcol2\x1b[0m\n=======|======\n\x1b[31mvalue1\x1b[0m | 2   "
        self.assertEqual(table, expected_table)


if __name__ == '__main__':
    unittest.main()
