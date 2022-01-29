from .token import Token
from .statement import Stmt


class OrderBy(Token):
    def __init__(self, col_name, order):
        super().__init__()
        self.col_name = col_name
        self.order = order

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} col_name='{self.col_name}' order='{self.order}'>"

    @classmethod
    def parse_action(cls, toks):
        return OrderBy(toks[0], toks[1])


class SelectStmt(Stmt):
    def __init__(self, distinct, select, from_table, where, group_by, having, order_by, limit, offset) -> None:
        super().__init__()
        self.distinct = distinct
        self.select = select
        self.from_table = from_table
        self.where = where
        self.group_by = group_by
        self.having = having
        self.order_by = order_by
        self.limit = limit
        self.offset = offset

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} " \
            f"distinct='{self.distinct}' " \
            f"select='{self.select}' " \
            f"from_table='{self.from_table}' " \
            f"where='{self.where}' " \
            f"group_by='{self.group_by}' " \
            f"having='{self.having}' " \
            f"order_by='{self.order_by}' " \
            f"limit='{self.limit}' " \
            f"offset='{self.offset}'>"

    @classmethod
    def parse_action(cls, toks):
        return SelectStmt(
            True if toks.distinct else False,
            toks.select, toks.from_table, toks.where,
            toks.group_by, toks.having, toks.order_by,
            toks.limit, toks.offset
        )
