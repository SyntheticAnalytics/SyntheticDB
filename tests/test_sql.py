# content of test_sample.py
from syntheticdb.query_parser import (
    Query,
    FloatRangeCondition,
    WhereClause,
    parse_sql_to_query,
)


def test_parse_table():
    assert parse_sql_to_query("select * from synth_user") == Query(
        table_name="synth_user", where_clauses=[], columns="*"
    )


def test_parse_where():
    assert parse_sql_to_query("select * from synth_user where height < 5") == Query(
        table_name="synth_user",
        where_clauses=[WhereClause("height", condition=FloatRangeCondition(None, 5))],
        columns="*",
    )


def test_parse_columns():
    assert parse_sql_to_query(
        "select age, height from synth_user where height < 5"
    ) == Query(
        table_name="synth_user",
        where_clauses=[WhereClause("height", condition=FloatRangeCondition(None, 5))],
        columns=["age", "height"],
    )


def test_db_join():
    business_table = Table(
        columns={
            "business_id": PrimaryKeyColumn(),
            "valuation": FloatColumn(Uniform(1_000_000, 1_000_000_000)),
        },
        row_count=10,
    )
    user_table = Table(
        columns={
            "user_id": PrimaryKeyColumn(),
            "income": FloatColumn(Uniform(20_000, 80_000)),
            "business_id": ForeignKeyColumn(
                foreign_table="business", foreign_column="business_id"
            ),
        },
        row_count=100,
    )
    db = DataBase(tables={"synth_user": user_table, "business": business_table})
    df = db.select(
        "select synth_user.income, business.valuation from synth_user "
        + "join business on synthetic_user.business_id == business.valuation"
    )
    assert df.columns
