import random
from dataclasses import dataclass
from typing import List, TypeVar, Generic, Tuple, Callable, Optional, Union, Dict
from functools import partial
from abc import ABC, abstractmethod
import pandas as pd
from scipy.stats import norm
from syntheticdb.db_core import Table, DataBase, Query, WhereClause, FloatRangeCondition
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

    rows = db.select("select * from `user`")
    df = pd.DataFrame.from_dict(rows)
    plot = pd.DataFrame(df)["height"].hist(bins=50)
    fig = plot.get_figure()
    fig.savefig("test2.png")
    print(df)
