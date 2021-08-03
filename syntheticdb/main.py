import random
from dataclasses import dataclass
from typing import List, TypeVar, Generic, Tuple, Callable, Optional, Union, Dict
from functools import partial
from abc import ABC, abstractmethod
import pandas as pd
from scipy.stats import norm

# T = TypeVar("T")
# class Column(ABC, Generic[T]):
#
#     def __init__(self, name: str):
#         self.name = name
#
#     @abstractmethod
#     def sample(self) -> T:
#         pass

@dataclass
class FloatRangeCondition:
    min: Optional[float]
    max: Optional[float]

T = TypeVar("T")
def sample_until(callable: Callable[[], T], condition: Callable[[T], bool]) -> T:
    while True:
        out_val = callable()
        if condition(out_val):
            return out_val

@dataclass(frozen=True)
class FloatColumn:
    sample: Callable[[], float]
    cdf: Callable[[float], float]

    def where(self, condition: FloatRangeCondition):
        if condition.min and condition.max:
            def new_cdf(point):
                cd_at_min = self.cdf(condition.min)
                cd_at_max = self.cdf(condition.max)
                if point < condition.min:
                    return 0
                if condition.min < point < condition.max:
                    return self.cdf(point) - cd_at_min
                if point > condition.max:
                    return cd_at_max

            return FloatColumn(
                sample=lambda: sample_until(self.sample, lambda x: condition.max > x > condition.min),
                cdf=new_cdf
            )
        if condition.min:
            def new_cdf(point):
                cd_at_min = self.cdf(condition.min)
                if point < condition.min:
                    return 0
                if condition.min < point:
                    return self.cdf(point) - cd_at_min
            return FloatColumn(
                sample=lambda: sample_until(self.sample, lambda x: x > condition.min),
                cdf=new_cdf
            )
        if condition.max:
            def new_cdf(point):
                cd_at_max = self.cdf(condition.max)
                if point < condition.max:
                    return self.cdf(point)
                if condition.max < point:
                    return cd_at_max
            return FloatColumn(
                sample=lambda: sample_until(self.sample, lambda x: x < condition.max),
                cdf=new_cdf
            )
        raise Exception("Invalid condition, must have at least one range value populated")

    def prob(self):
        return self.cdf(1e10)




def uniform_cdf(min_val: float, max_val: float, point: float) -> float:
    if point < min_val:
        return 0
    if min_val < point < max_val:
        return (point - min_val) / (max_val - min_val)
    if point > max_val:
        return 1

def uniform_float_column(min: float, max:float) -> FloatColumn:
    return FloatColumn(
        sample=lambda: (random.random() * max-min) + min,
        cdf=partial(uniform_cdf, min, max)
    )

def standard_normal_float_column(mean: float, std_dev: float) -> FloatColumn:
    dist = norm(loc=mean, scale=std_dev)
    return FloatColumn(
        sample=dist.rvs,
        cdf=dist.cdf
    )

@dataclass
class WhereClause:
    column_name: str
    condition: Union[FloatRangeCondition]

@dataclass
class Query:
    table_name: str
    where_clauses: List[WhereClause]

@dataclass(frozen=True)
class Table:
    columns: Dict[str, Union[FloatColumn]]
    row_count: int

    def get_row_num(self) -> int:
        probability = 1
        for column in self.columns.values():
            probability = probability * column.prob()
        return int(self.row_count * probability)


def select(table: Table, where_clauses: List[WhereClause]):
    view_table = Table(table.columns, table.row_count)
    for clause in where_clauses:
        column = view_table.columns.get(clause.column_name, None)
        if column is None:
            raise Exception(f"column with name: {clause.column_name}, does not exist")
        if type(clause.condition) not in [FloatRangeCondition]:
            raise Exception(f"Condition type not supported")
        if type(clause.condition) == FloatRangeCondition:
            view_table.columns[clause.column_name] = column.where(clause.condition)
    new_row_count = view_table.get_row_num()
    return {name: [col.sample() for _ in range(new_row_count)] for name, col in view_table.columns.items()}


if __name__ == "__main__":
    table = Table(
        columns={
            "age": uniform_float_column(0, 100),
            "height": standard_normal_float_column(5, 1)
        },
        row_count=1000
    )
    rows = select(table, where_clauses=[
        WhereClause(column_name="age", condition=FloatRangeCondition(None, 30)),
        WhereClause(column_name="height", condition=FloatRangeCondition(None, 5))
    ])
    df = pd.DataFrame.from_dict(rows)
    plot = pd.DataFrame(df)["height"].hist(bins=50)
    fig = plot.get_figure()
    fig.savefig("test2.png")
    print(df)