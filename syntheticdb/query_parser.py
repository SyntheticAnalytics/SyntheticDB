from dataclasses import dataclass
from typing import List, Optional, Union, Tuple, Callable
import sqlparse
from sqlparse.sql import IdentifierList, Token, Identifier, Where, Comparison
from functools import partial


@dataclass
class FloatRangeCondition:
    min: Optional[float]
    max: Optional[float]


@dataclass
class WhereClause:
    column_name: str
    condition: Union[FloatRangeCondition]


@dataclass
class Query:
    table_name: str
    columns: Union[List[str], str]
    where_clauses: List[WhereClause]


# def parse_sql_to_query(raw: str) -> Query:
#     parsed = sqlparse.parse(raw)[0]
#     important_tokens = [token for token in parsed if token.is_whitespace is False]
#     from_position = -1
#     for i, token in enumerate(important_tokens):
#         if token.normalized == "FROM":
#             from_position = i
#     table_name: str = important_tokens[from_position + 1].value
#     table_name = table_name.strip("`")
#     where_position = -1
#     for i, token in enumerate(important_tokens):
#         if token.normalized == "WHERE":
#             where_position = i
#
#     return Query(
#         table_name=table_name,
#         columns=[""],
#         where_clauses=[]
#     )


def query(
    columns: Union[List[str], str],
    table_name: str,
    where_clauses: List[WhereClause],
) -> Query:
    return Query(table_name=table_name, columns=columns, where_clauses=where_clauses)


parser = Callable[[partial, List[Token]], Tuple[partial, List[Token]]]


def parse_select(parse: partial, tokens: List[Token]) -> Tuple[partial, List[Token]]:
    if tokens[0].normalized == "SELECT":
        return parse, tokens[1:]
    else:
        raise Exception("SQL query must start with a select")


def parse_columns(parse: partial, tokens: List[Token]) -> Tuple[partial, List[Token]]:
    token = tokens[0]
    if token.normalized == "*":
        return partial(parse, "*"), tokens[1:]
    elif type(token) == Identifier:
        identifier_list = [token.normalized]
        return partial(parse, identifier_list), tokens[1:]
    elif type(token) == IdentifierList:
        identifier_list = [
            tok.normalized for tok in token.tokens if type(tok) == Identifier
        ]
        return partial(parse, identifier_list), tokens[1:]
    else:
        raise Exception("Must specify columns")


def parse_from(parse: partial, tokens: List[Token]) -> Tuple[partial, List[Token]]:
    if tokens[0].normalized == "FROM":
        return parse, tokens[1:]
    else:
        raise Exception("Columns must be followed by a FROM clause")


def parse_table(parse: partial, tokens: List[Token]) -> Tuple[partial, List[Token]]:
    if type(tokens[0]) == Identifier:
        parse = partial(parse, tokens[0].normalized)
        return parse, tokens[1:]
    else:
        raise Exception("From statement must be followed by a table name")


def parse_where(parse: partial, tokens: List[Token]) -> Tuple[partial, List[Token]]:
    next = tokens[0]
    if type(next) == Where:
        where_tokens = next.tokens
        comparisons = [tok for tok in where_tokens if type(tok) == Comparison]
        conditions = []
        for comparison in comparisons:
            column = comparison.left.normalized
            num = float(comparison.right.normalized)
            comparator = comparison.tokens[2].normalized
            if comparator == "<":
                conditions.append(WhereClause(column, FloatRangeCondition(None, num)))
            elif comparator == ">":
                conditions.append(WhereClause(column, FloatRangeCondition(num, None)))
        return partial(parse, conditions), tokens[1:]
    else:
        raise Exception(
            "Where select statement must either terminate or be followed by a where clause"
        )


def parse_sql_to_query(raw: str) -> Query:
    parsed = sqlparse.parse(raw)[0]
    tokens = [token for token in parsed if token.is_whitespace is False]
    parse = partial(query)
    parse, tokens = parse_select(parse, tokens)
    parse, tokens = parse_columns(parse, tokens)
    parse, tokens = parse_from(parse, tokens)
    parse, tokens = parse_table(parse, tokens)
    if len(tokens) == 0:
        parse = partial(parse, [])
        return parse()
    parse, tokens = parse_where(parse, tokens)
    return parse()


@dataclass
class ParseResult:
    success: bool
    query_inputs: List[Token]
    query_result: Optional[Query]


if __name__ == "__main__":
    print(
        parse_sql_to_query(
            "select age, height from synth_user where age > 5 and height < 2"
        )
    )
