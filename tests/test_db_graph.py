from syntheticdb.graph import (
    DBGraph,
    DistributionColumnNode,
    PrimaryKeyColumnNode,
    ForeignKeyColumnNode,
    TableNode,
    Query,
    Select,
    DoubleColDelimiter,
    Join,
    Table,
    From,
    validate,
)


def get_test_graph() -> DBGraph:
    val_node_1 = DistributionColumnNode("num_employees")
    pk_1 = PrimaryKeyColumnNode("company_id")
    tbl_1 = TableNode("company", columns=[val_node_1, pk_1])
    val_node_2 = DistributionColumnNode("income")
    pk_2 = PrimaryKeyColumnNode("employee_id")
    fk_2 = ForeignKeyColumnNode("company_id", primary_key=pk_1)
    tbl_2 = TableNode("employee", columns=[val_node_2, pk_2, fk_2])
    return DBGraph(nodes=[val_node_1, pk_1, tbl_1, val_node_2, pk_2, fk_2, tbl_2])


def get_test_query() -> Query:
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


def test_query_validator():
    db = get_test_graph()
    query = get_test_query()
    assert validate(db, query)
