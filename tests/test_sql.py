# content of test_sample.py
from syntheticdb.db_core import Query, parse_sql_to_query

def test_parse():
    assert parse_sql_to_query("select * from user") == Query(table_name="user", where_clauses=[])