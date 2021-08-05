import pandas as pd
from syntheticdb.db_core import Table, DataBase
from syntheticdb.distributions import uniform_float_column, standard_normal_float_column


if __name__ == "__main__":
    user_table = Table(
        columns={
            "age": uniform_float_column(0, 100),
            "height": standard_normal_float_column(5, 1),
        },
        row_count=1000,
    )
    db = DataBase(tables={"user": user_table})

    df = db.select("select * from `user` where height > 2 and age < 20")
    plot = df["age"].hist(bins=50)
    fig = plot.get_figure()
    fig.savefig("test2.png")
    print(df)
