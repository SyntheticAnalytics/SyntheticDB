from dataclasses import dataclass
from typing import List, TypeVar, Callable, Optional, Union, Dict
import sqlparse


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
                sample=lambda: sample_until(
                    self.sample, lambda x: condition.max > x > condition.min
                ),
                cdf=new_cdf,
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
                cdf=new_cdf,
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
                cdf=new_cdf,
            )
        raise Exception(
            "Invalid condition, must have at least one range value populated"
        )

    def prob(self):
        return self.cdf(1e10)


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


@dataclass
class Query:
    table_name: str
    where_clauses: List[WhereClause]

def parse_sql_to_query(raw: str) -> Query:
    parsed = sqlparse.parse(raw)[0]
    important_tokens = [token for token in parsed if token.is_whitespace is False]
    from_position = -1
    for i, token in enumerate(important_tokens):
        if token.normalized == "FROM":
            from_position = i
    table_name: str = important_tokens[from_position + 1].value
    table_name = table_name.strip("`")
    return Query(
        table_name=table_name,
        where_clauses=[]
    )

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
        table = self.tables.get(table_name)
        view_table = Table(table.columns, table.row_count)
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
        return {
            name: [col.sample() for _ in range(new_row_count)]
            for name, col in view_table.columns.items()
        }