from .token import Token


class Identifier(Token):
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.value}'>"

    def eval(self, context):
        pass

    @classmethod
    def parse_action(cls, toks):
        return cls(toks[0])


class TableName(Identifier):
    pass


class ColName(Identifier):
    pass


class RowName(Identifier):
    pass


class FuncName(Identifier):
    def eval(self, context):
        return self.value
