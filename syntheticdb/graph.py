import functools
from dataclasses import dataclass
from typing import List, Type, Callable, Union, TypeVar, Dict, Tuple, Iterable, NewType
from abc import ABC, abstractmethod

import pandas
import pandas as pd
import random
from scipy.stats import uniform
from itertools import count, cycle


class Column(ABC):
    def __init__(self, name: str):
        self.name = name


class Uniform:
    def __init__(self, loc: float, scale: float):
        self.dist = uniform(loc=loc, scale=scale)

    def sample(self) -> float:
        return self.dist.rvs()

    def cdf(self, at: float) -> float:
        return self.dist.cdf(at)


Distribution = Union[Uniform]


class DistributionColumn(Column):
    def __init__(self, name: str, distribution: Distribution):
        super().__init__(name)
        self.distribution = distribution

    def sample(self):
        return self.distribution.sample()

    def cdf(self, at):
        return self.distribution.cdf(at)


class PrimaryKeyColumn(Column):
    def __init__(self, name: str):
        super().__init__(name)


class ForeignKeyColumn(Column):
    def __init__(self, name: str, other_table: str, other_column: str):
        super().__init__(name)
        self.other_table = other_table
        self.other_column = other_column


@dataclass
class TableView:
    sample: Callable[[], pd.DataFrame]


#
#
# class Table:
#     def __init__(
#         self,
#         name: str,
#         row_count: int,
#         pk_column: PrimaryKeyColumn,
#         fk_columns: List[ForeignKeyColumn],
#         dist_columns: List[DistributionColumn],
#     ):
#         self.name = name
#         self.row_count = row_count
#         self.pk_column = pk_column
#         self.fk_columns = fk_columns
#         self.dist_columns = dist_columns

# @dataclass
# class Database:
#     tables: Dict[str, Table]
#
#
#     def sample_from(self, table_name: str) -> pd.DataFrame:
#         table = self.tables.get(table_name)
#         if table is None:
#             raise Exception("Invalid Table Name")
#         col_iters = []
#         col_iters.append((table.pk_column.name, (i for i in range(1, table.row_count + 1))))
#         for fk in table.fk_columns:
#             foreign_table = self.tables.get(fk.other_table)
#             fk_iter = cycle(range(1, foreign_table.row_count))
#             col_iters.append((fk.name, fk_iter))
#         col_iters += [(col.name, (col.sample() for _ in count())) for col in table.dist_columns]
#         for row in range(table.row_count):
#             out_dict = {key: [next(val_iter)] for key, val_iter in col_iters}
#             df = pd.DataFrame(out_dict)
#             yield df
#
#     def select_star(self, table_name: str):
#         dfs = []
#         for df in self.sample_from(table_name):
#             dfs.append(df)
#         return pandas.concat(dfs)
#
#
#
#
#
# pk1 = PrimaryKeyColumn("test_pk_1")
# val_key_1 = DistributionColumn("test_val_key", distribution=Uniform(0, 10))
# t1 = Table("test_table_1",row_count=100, pk_column=pk1, fk_columns=[],  dist_columns=[val_key_1])
# pk2 = PrimaryKeyColumn("test_pk_2")
# val_key_2 = DistributionColumn("test_val_key_2", distribution=Uniform(5, 10))
# fk_2 = ForeignKeyColumn("test_fk", other_table="test_table_1", other_column="test_pk_1")
# t2 = Table("test_table_2", row_count=100, pk_column=pk2, fk_columns=[fk_2], dist_columns=[val_key_2])
# db = Database({"test_table_1": t1, "test_table_2" : t2})
# print(db.select_star("test_table_2"))
#

#
#
# def join(t1: Table, t2: Table, join_cols: Tuple[str, str]):
#     table_col_map = {t.name: t.columns for t in [t1, t2]}
#     first_col = join_cols[0].split(".")
#     second_col = join_cols[1].split(".")


@dataclass
class DistributionColumnNode:
    name: str


@dataclass
class PrimaryKeyColumnNode:
    name: str


@dataclass
class ForeignKeyColumnNode:
    name: str
    primary_key: PrimaryKeyColumnNode


@dataclass
class TableNode:
    name: str
    columns: List[
        Union[DistributionColumnNode, PrimaryKeyColumnNode, ForeignKeyColumnNode]
    ]


@dataclass
class DBGraph:
    nodes: List[
        Union[
            TableNode,
            DistributionColumnNode,
            PrimaryKeyColumnNode,
            ForeignKeyColumnNode,
        ]
    ]


def get_test_graph() -> DBGraph:
    val_node_1 = DistributionColumnNode("num_employees")
    pk_1 = PrimaryKeyColumnNode("company_id")
    tbl_1 = TableNode("company", columns=[val_node_1, pk_1])
    val_node_2 = DistributionColumnNode("income")
    pk_2 = PrimaryKeyColumnNode("employee_id")
    fk_2 = ForeignKeyColumnNode("company_id", primary_key=pk_1)
    tbl_2 = TableNode("employee", columns=[val_node_2, pk_2, fk_2])
    return DBGraph(nodes=[val_node_1, pk_1, tbl_1, val_node_2, pk_2, fk_2, tbl_2])


graph = get_test_graph()


@dataclass
class SingleColDelimiter:
    col: str


@dataclass
class DoubleColDelimiter:
    table: str
    col: str


@dataclass
class Select:
    cols: List[DoubleColDelimiter]


Table = NewType("Table", str)


@dataclass
class Join:
    tables: Tuple[Table, Table]
    # Assuming join on column equality
    cols: Tuple[DoubleColDelimiter, DoubleColDelimiter]


@dataclass
class From:
    table_view: Union[Table, Join]


@dataclass
class Query:
    select_clause: Select
    from_clause: From


def get_test_query():
    # SELECT employee.employee_id, employee.income, company.num_employees
    #     FROM employee JOIN company ON employee.company_id = company.company_id
    return Query(
        select_clause=Select(
            cols=[
                DoubleColDelimiter(table="employee", col="employee_id"),
                DoubleColDelimiter(table="employee", col="income"),
                DoubleColDelimiter(table="company", col="num_employees"),
            ]
        ),
        from_clause=From(
            table_view=Join(
                tables=(Table("employee"), Table("company")),
                cols=(
                    DoubleColDelimiter(table="employee", col="company_id"),
                    DoubleColDelimiter(table="company", col="company_id"),
                ),
            )
        ),
    )


def validate(db_graph: DBGraph, query: Query) -> bool:
    pass
