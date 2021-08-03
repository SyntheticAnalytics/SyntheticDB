# content of test_sample.py
from syntheticdb.sql_engine import parse_sql_to_query
from syntheticdb.db_core import Query

def test_parse():
    assert parse_sql_to_query("select * from user") == Query(table_name="user", where_clauses=[])