import pyparsing as pp
from . import keyword as kw
from . import symbol as sym
from .token import Token
from .identifier import col_name, table_name
from .literal import wildcard_all
from .expr import where_expr, having_expr


# select_stmt =  pp.Keyword('select') + select_expr('select_cols')  \
#     + pp.Keyword('from') + table_name('from_table') \
#     + pp.Optional(pp.Keyword('order') + pp.Keyword('by') + order_list('order_by')) \
#     + scolon

class OrderBy(Token):
    def __init__(self, col_name, order):
        super().__init__()
        self.col_name = col_name
        self.order = order

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} col_name='{self.order}' col_name='{self.order}'>"

    @classmethod
    def parse_action(cls, toks):
        return OrderBy(toks[0], toks[1])

# Change Token to Stmt
class SelectStmt(Token):
    def __init__(self, select, from_table, where, group_by, having, order_by) -> None:
        super().__init__()
        self.select = select
        self.from_table = from_table
        self.where = where
        self.group_by = group_by
        self.having = having
        self.order_by = order_by

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} " \
            f"select='{self.select}' " \
            f"from_table='{self.from_table}' " \
            f"where='{self.where}' " \
            f"group_by='{self.group_by}' " \
            f"having='{self.having}' " \
            f"order_by='{self.order_by}'>"

    @classmethod
    def parse_action(cls, toks):
        return SelectStmt(
            toks.select, toks.from_table, toks.where,
            toks.group_by, toks.having, toks.order_by
        )


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
