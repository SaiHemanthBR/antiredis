import pyparsing as pp
from . import keyword as kw
from . import symbol as sym
from ..classes.select_stmt import SelectStmt, OrderBy
from .identifier import col_name, table_name
from .literal import wildcard_all
from .expression import where_expr, having_expr


select_expr = wildcard_all | pp.delimited_list(col_name)

order_expr = col_name + pp.Optional(kw.ASC | kw.DESC, default=kw.ASC)
order_expr.set_parse_action(OrderBy.parse_action)
order_list = pp.delimited_list(order_expr)

group_list = pp.delimited_list(col_name)

select_stmt = (
    kw.SELECT + select_expr('select')
    + kw.FROM + table_name('from_table')
    + pp.Optional(kw.WHERE + where_expr('where'))
    + pp.Optional(
        kw.GROUP + kw.BY + group_list('group_by')
        + pp.Optional(kw.HAVING + having_expr('having'))
    )
    + pp.Optional(kw.ORDER + kw.BY + order_list('order_by'))
    + sym.SCOLON
)
select_stmt.set_parse_action(SelectStmt.parse_action)

if __name__ == '__main__':
    test = "select * from table1 where x > 5 and y < -1 group by x having z > 5 order by x, y desc;"
    res = select_stmt.parse_string(test)

    print(res)
