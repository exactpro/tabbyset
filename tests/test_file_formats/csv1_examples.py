from enum import Enum


class Csv1Examples(Enum):
    valid_new_id = """
TEST_CASE_START
name
2e9b7b8c-2d9f-4f65-858a-1bb339885e23
description
A,B,C
1,2,3
4,5,6
TEST_CASE_END
"""
    valid = """
TEST_CASE_START
name
instrument
description
A,B,C
1,2,3
4,5,6
TEST_CASE_END
"""
    invalid_double_start = """
TEST_CASE_START
name
instrument
description
TEST_CASE_START
A,B,C
1,2,3
4,5,6
TEST_CASE_END
"""
    invalid_double_end = """
TEST_CASE_START
name
instrument
description
A,B,C
1,2,3
4,5,6
TEST_CASE_END

TEST_CASE_END
"""
    invalid_no_name = """
TEST_CASE_START

instrument
description
A,B,C
1,2,3
4,5,6
TEST_CASE_END
"""
    invalid_no_instrument = """
TEST_CASE_START
name

description
A,B,C
1,2,3
4,5,6
TEST_CASE_END
"""
    valid_instrument_only_in_rows = """
TEST_CASE_START
name

description
A,B,C,Symbol
1,2,3,instrument
4,5,6,instrument
TEST_CASE_END
"""
    valid_no_description = """
TEST_CASE_START
name
instrument

A,B,C
1,2,3
4,5,6
TEST_CASE_END
"""
    invalid_extra_valuable_values = """
TEST_CASE_START
name
instrument
description
A,B,C
1,2,3,extra
4,5,6
TEST_CASE_END
"""
    valid_extra_empty_values = """
TEST_CASE_START
name
instrument
description
A,B,C
1,2,3,,,
4,5,6
TEST_CASE_END
"""
    valid_not_enough_values = """
TEST_CASE_START
name
instrument
description
A,B,C
1,2
4,5,6
TEST_CASE_END
"""
    invalid_test_case_not_closed = """
TEST_CASE_START
name
instrument
description
A,B,C
1,2,3
4,5,6
"""
    valid_no_table = """
TEST_CASE_START
name
instrument
description
TEST_CASE_END
"""
    valid_nameless_column = """
TEST_CASE_START
name
instrument
description
A,B,
1,2,3
4,5,6
TEST_CASE_END
"""
