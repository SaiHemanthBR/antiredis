from .token import Token


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
