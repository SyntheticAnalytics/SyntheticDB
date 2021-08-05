# content of test_sample.py
from syntheticdb.query_parser import (
    Query,
    FloatRangeCondition,
    WhereClause,
    parse_sql_to_query,
)


def test_parse_table():
    assert parse_sql_to_query("select * from synth_user") == Query(
        table_name="synth_user", where_clauses=[]
    )


def test_parse_where():
    assert parse_sql_to_query("select * from synth_user where height < 5") == Query(
        table_name="synth_user",
        where_clauses=[WhereClause("height", condition=FloatRangeCondition(None, 5))],
    )
