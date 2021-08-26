from syntheticdb.db_core import (
    PrimaryKeyColumn,
    FloatColumn,
    ForeignKeyColumn,
    Table,
    DataBase,
)
from syntheticdb.distributions import Uniform


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
    assert len(df.columns)
