import sqlparse
from syntheticdb.db_core import Query

def parse_sql_to_query(raw: str) -> Query:
    parsed = sqlparse.parse(raw)[0]
    important_tokens = [token for token in parsed if token.is_whitespace is False]
    from_position = -1
    for i, token in enumerate(important_tokens):
        if token.normalized == "FROM":
            from_position = i
    table_name = important_tokens[from_position + 1].value
    return Query(
        table_name=table_name,
        where_clauses=[]
    )

if __name__ == "__main__":
    print(parse_sql_to_query("select * from 'user'"))