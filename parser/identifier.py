import pyparsing as pp
from pyparsing import pyparsing_common as ppc
from . import keyword as kw
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


quoted_identifier = pp.QuotedString('`')
identifier = (
    (~kw.any_keyword + pp.Word(pp.alphas, pp.alphanums + '_')
     ).set_parse_action(ppc.downcase_tokens)
    | quoted_identifier
).set_parse_action(Identifier.parse_action)
table_name = identifier().set_parse_action(TableName.parse_action)
col_name = identifier().set_parse_action(ColName.parse_action)
row_name = identifier().set_parse_action(RowName.parse_action)
func_name = identifier().set_parse_action(FuncName.parse_action)

if __name__ == "__main__":
    print(identifier.parse_string('xyz'))
    # print(identifier.parse_string('select'))
