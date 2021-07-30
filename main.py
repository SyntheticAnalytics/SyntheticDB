import random
from dataclasses import dataclass
from typing import List, TypeVar, Generic, Tuple
from abc import ABC, abstractmethod
import pandas as pd

T = TypeVar("T")
class Column(ABC, Generic[T]):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def sample(self) -> T:
        pass


class UniformIntColumn(Column):

    def __init__(self, name: str, range: Tuple[int, int]):
        super().__init__(name)
        self.range = range
        self.range_size = range[1] - range[0]

    def prob_greater_than(self, lower_limit: int):
        if self.range[1] - lower_limit <= 0:
            return 1
        diff_over_lower = lower_limit - self.range[0]
        if diff_over_lower <= 0:
            return 0
        return (self.range_size - diff_over_lower)/self.range_size

    def sample(self, lower_limit: int):
        return random.randint(lower_limit, self.range[1])


@dataclass
class Table:
    columns: List[UniformIntColumn]
    row_count: int


    def get_row_num(self, where: Tuple[UniformIntColumn, str, int]) -> int:
        column = where[0]
        comparison_operator = where[1]
        bound = where[2]
        if column not in self.columns:
            raise Exception("Column in where clause not in tables columns")
        if comparison_operator != ">":
            raise Exception("Comparison operator not supported")
        return int(self.row_count * column.prob_greater_than(bound))


    def select(self, where: Tuple[UniformIntColumn, str, int]):
        new_row_count = self.get_row_num(where)
        return {col.name: [col.sample(where[2]) for i in range(new_row_count)] for col in self.columns}


if __name__ == "__main__":
    table = Table(columns=[UniformIntColumn("Age", range=(0, 100)), UniformIntColumn("Height", range=(0, 50))], row_count=10)
    rows = table.select((table.columns[0], ">", 40))
    df = pd.DataFrame.from_dict(rows)
    print(df)