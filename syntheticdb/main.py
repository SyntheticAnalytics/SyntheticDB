import pandas as pd
from syntheticdb.db_core import Table, DataBase, FloatColumn
from syntheticdb.distributions import Uniform, LogUniform, Normal, LogNormal, Gamma, Exponential, Beta, Weibull

if __name__ == "__main__":
    dist_table = Table(
        columns={
            "unif": FloatColumn(Uniform(0,1)),
            "logUnif": FloatColumn(LogUniform(0.01,1.25)),
            "norm": FloatColumn(Normal(0,1)),
            "logNorm": FloatColumn(LogNormal(1,0,1)),
            "gamma": FloatColumn(Gamma(2,0,1)),
            "exp": FloatColumn(Exponential(0,1)),
            "beta": FloatColumn(Beta(2,3)),
            "wei": FloatColumn(Weibull(2,0,1)),
        },
        row_count=100,
    )
    db = DataBase(tables={"dist": dist_table})
    df = db.select("select * from dist")
    plot = df["unif"].hist(bins=50)
    fig = plot.get_figure()
    fig.savefig("test.png")

    print(df)
    