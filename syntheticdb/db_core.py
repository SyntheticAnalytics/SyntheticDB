from dataclasses import dataclass
from typing import List, TypeVar, Callable, Union, Dict
from copy import deepcopy
import pandas as pd

from syntheticdb.query_parser import Query, FloatRangeCondition, parse_sql_to_query

T = TypeVar("T")


def sample_until(callable: Callable[[], T], condition: Callable[[T], bool]) -> T:
    while True:
        out_val = callable()
        if condition(out_val):
            return out_val

@dataclass
class Distribution:
    sample: Callable[[], float]
    cdf: Callable[[float], float]

@dataclass(frozen=True)
class FloatColumn:
    distribution: Distribution

    def where(self, condition: FloatRangeCondition):
        if condition.min and condition.max:

            def new_cdf(point):
                cd_at_min = self.distribution.cdf(condition.min)
                cd_at_max = self.distribution.cdf(condition.max)
                if point < condition.min:
                    return 0
                if condition.min < point < condition.max:
                    return self.distribution.cdf(point) - cd_at_min
                if point > condition.max:
                    return cd_at_max

            return FloatColumn(
                Distribution(
                    sample=lambda: sample_until(self.distribution.sample, lambda x: condition.max > x > condition.min),
                    cdf=new_cdf,
                )
            )
        if condition.min:

            def new_cdf(point):
                cd_at_min = self.distribution.cdf(condition.min)
                if point < condition.min:
                    return 0
                if condition.min < point:
                    return self.distribution.cdf(point) - cd_at_min

            return FloatColumn(
                Distribution(
                    sample=lambda: sample_until(self.distribution.sample, lambda x: x > condition.min),
                    cdf=new_cdf,
                )
            )
        if condition.max:

            def new_cdf(point):
                cd_at_max = self.distribution.cdf(condition.max)
                if point < condition.max:
                    return self.distribution.cdf(point)
                if condition.max < point:
                    return cd_at_max

            return FloatColumn(
                Distribution(
                    sample=lambda: sample_until(self.distribution.sample, lambda x: x < condition.max),
                    cdf=new_cdf,
                )
            )
        raise Exception(
            "Invalid condition, must have at least one range value populated"
        )

    def prob(self):
        return self.distribution.cdf(1e10)


@dataclass(frozen=True)
class Table:
    columns: Dict[str, Union[FloatColumn]]
    row_count: int

    def get_row_num(self) -> int:
        probability = 1
        for name, column in self.columns.items():
            probability = probability * column.prob()
        return int(self.row_count * probability)


@dataclass
class DataBase:
    tables: Dict[str, Table]

    def select(self, query_text: str):
        query = parse_sql_to_query(query_text)
        result = self.select_from_query(query)
        return result

    def select_from_query(self, query: Query) -> Dict[str, List[float]]:
        table_name = query.table_name
        where_clauses = query.where_clauses
        stripped_table_name = table_name.strip("`")
        table = self.tables.get(stripped_table_name)
        view_table = deepcopy(table)
        for clause in where_clauses:
            column = view_table.columns.get(clause.column_name, None)
            if column is None:
                raise Exception(
                    f"column with name: {clause.column_name}, does not exist"
                )
            if type(clause.condition) not in [FloatRangeCondition]:
                raise Exception(f"Condition type not supported")
            if type(clause.condition) == FloatRangeCondition:
                view_table.columns[clause.column_name] = column.where(clause.condition)
        new_row_count = view_table.get_row_num()
        columns_to_return = {}
        if query.columns == "*":
            for name, col in view_table.columns.items():
                columns_to_return[name] = [col.distribution.sample() for _ in range(new_row_count)]
        else:
            for name, col in view_table.columns.items():
                if name in query.columns:
                    columns_to_return[name] = [
                        col.distribution.sample() for _ in range(new_row_count)
                    ]
        return pd.DataFrame.from_dict(columns_to_return)
