import pyparsing as pp
from . import keyword as kw
from . import symbol as sym
from ..classes.select_stmt import SelectStmt, OrderBy
from .identifier import col_name, table_name
from .literal import wildcard_all, numeric_literal
from .expression import expr, bool_expr


select_expr = wildcard_all | pp.delimited_list(expr, min=1)

where_expr = bool_expr()
having_expr = bool_expr()

group_list = pp.delimited_list(expr)

order_expr = expr + pp.Optional(kw.ASC | kw.DESC, default=kw.ASC)
order_expr.set_parse_action(OrderBy.parse_action)
order_list = pp.delimited_list(order_expr)

select_stmt = (
    kw.SELECT
    + pp.Optional(kw.DISTINCT)('distinct')
    + select_expr('select')
    + kw.FROM + table_name('from_table')
    + pp.Optional(kw.WHERE + where_expr('where'))
    + pp.Optional(
        kw.GROUP + kw.BY + group_list('group_by')
        + pp.Optional(kw.HAVING + having_expr('having'))
    )
    + pp.Optional(kw.ORDER + kw.BY + order_list('order_by'))
    + pp.Optional(
        kw.LIMIT + numeric_literal('limit')
        + pp.Optional(kw.OFFSET + numeric_literal('offset'))
    )
    + sym.SCOLON
)
select_stmt.set_parse_action(SelectStmt.parse_action)

if __name__ == '__main__':
    test = "select sum(x) from table1 where x > 5 and y < -1 group by x having z > 5 order by x, y desc limit 5 offset 3;"
    res = select_stmt.parse_string(test)

    print(res)
