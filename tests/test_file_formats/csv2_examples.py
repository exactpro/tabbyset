from enum import Enum


class Csv2Examples(Enum):
    valid = """
A,B,C,D,E
TEST_CASE_START,name1
A,B,,D,
1,2,,3,
4,5,,6,
TEST_CASE_END
TEST_CASE_START,name2
,B,C,,E
,1,2,,3
,4,5,,6
TEST_CASE_END
"""
    invalid_no_header = """
TEST_CASE_START,name1
A,B,,D,
1,2,,3,
4,5,,6,
TEST_CASE_END
TEST_CASE_START,name2
,B,C,,E
,1,2,,3
,4,5,,6
TEST_CASE_END
"""
    invalid_double_start = """
A,B,C,D,E
TEST_CASE_START,name1
A,B,,D,
TEST_CASE_START
1,2,,3,
4,5,,6,
TEST_CASE_END
"""
    invalid_double_end = """
A,B,C,D,E
TEST_CASE_START,name1
A,B,,D,
1,2,,3,
4,5,,6,
TEST_CASE_END
TEST_CASE_END
"""
    invalid_no_name = """
A,B,C,D,E
TEST_CASE_START,
A,B,,D,
1,2,,3,
4,5,,6,
TEST_CASE_END
"""
    invalid_header_single_element = """
A,B,C,D,E
TEST_CASE_START
A,B,,D,
1,2,,3,
4,5,,6,
TEST_CASE_END
"""
    invalid_extra_case_column = """
A,B,C,D,E
TEST_CASE_START,name1
A,B,,D,,EXTRA
1,2,,3,
4,5,,6,
TEST_CASE_END
"""
    valid_extra_empty_case_column = """
A,B,C,D,E
TEST_CASE_START,name1
A,B,,D,,,,,
1,2,,3,
4,5,,6,
TEST_CASE_END
"""
    valid_less_case_columns_than_global_columns = """
A,B,C,D,E
TEST_CASE_START,name1
A,B
1,2
4,5
TEST_CASE_END
"""
    valid_extra_empty_values = """
A,B,C,D,E
TEST_CASE_START,name1
A,B,,D,
1,2,,3,,,,,,
4,5,,6,,,,,
TEST_CASE_END
TEST_CASE_START,name2
,B,C,,E
,1,2,,3
,4,5,,6
TEST_CASE_END
"""
    valid_not_enough_values = """
A,B,C,D,E
TEST_CASE_START,name1
A,B,,D,
1,2,,
4,5,,6,
TEST_CASE_END
TEST_CASE_START,name2
,B,C,,E
,1,2,,3
,4,5,,6
TEST_CASE_END
"""
    invalid_test_case_not_closed = """
A,B,C,D,E
TEST_CASE_START,name1
A,B,,D,
1,2,,3,
4,5,,6,
"""
    valid_no_table = """
A,B,C,D,E
TEST_CASE_START,name1
TEST_CASE_END
"""
    valid_nameless_column = """
A,B,C,D,E
TEST_CASE_START,name1
A,B,,,
1,2,,3,
4,5,,6,
TEST_CASE_END
"""
    valid_multiheader = """
Category,#category:a,A,B,D,HeaderDefinition,HeaderDefinitionCategories:a
Category,#category:b,B,C,E,HeaderDefinition,HeaderDefinitionCategories:b
TEST_CASE_START,name1
a,#category:a,1,2,3
b,#category:b,4,5,6
TEST_CASE_END
TEST_CASE_START,name2
b,#category:b,1,2,3
a,#category:a,4,5,6
TEST_CASE_END
"""
    valid_multiheader_too_much_values = """
Category,#category:a,A,B,D,HeaderDefinition,HeaderDefinitionCategories:a
Category,#category:b,B,C,E,HeaderDefinition,HeaderDefinitionCategories:b
TEST_CASE_START,name1
a,#category:a,1,2,3,999,999
b,#category:b,4,5,6,999,999
TEST_CASE_END
"""
    valid_multiheader_less_values = """
Category,#category:a,A,B,D,HeaderDefinition,HeaderDefinitionCategories:a
Category,#category:b,B,C,E,HeaderDefinition,HeaderDefinitionCategories:b
TEST_CASE_START,name1
a,#category:a,1,2
b,#category:b,4,5
TEST_CASE_END
"""
    invalid_multiheader_empty_category_value = """
Category,#category:a,A,B,D,HeaderDefinition,HeaderDefinitionCategories:a
Category,#category:b,B,C,E,HeaderDefinition,HeaderDefinitionCategories:b
TEST_CASE_START,name1
a,,1,2,3
b,,4,5,6
TEST_CASE_END
TEST_CASE_START,name2
b,,1,2,3
a,,4,5,6
TEST_CASE_END
"""
    invalid_multiheader_misleading_category_value = """
Category,#category:a,A,B,D,HeaderDefinition,HeaderDefinitionCategories:a
Category,#category:b,B,C,E,HeaderDefinition,HeaderDefinitionCategories:b
TEST_CASE_START,name1
b,#category:a,1,2,3
a,#category:b,4,5,6
TEST_CASE_END
TEST_CASE_START,name2
a,#category:b,1,2,3
b,#category:a,4,5,6
TEST_CASE_END
"""

    invalid_multiheader_undefined_category = """
Category,#category:a,A,B,D,HeaderDefinition,HeaderDefinitionCategories:a
TEST_CASE_START,name1
a,#category:a,1,2,3
b,#category:b,4,5,6
TEST_CASE_END
TEST_CASE_START,name2
b,#category:b,1,2,3
a,#category:a,4,5,6
TEST_CASE_END
"""
