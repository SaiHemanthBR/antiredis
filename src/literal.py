import pyparsing as pp
from pyparsing import pyparsing_common as ppc
from .token import Token
from . import symbol as sym
from . import keyword as kw

class WildcardAll(Token):
    pass

class NumericLiteral(Token):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    def eval(self):
        return self.value

    @classmethod
    def parse_action(cls, toks):
        return NumericLiteral(toks[0])

wildcard_all = pp.Literal('*')
wildcard_all.set_parse_action(WildcardAll.parse_action)

numeric_literal = ppc.number.set_parse_action(NumericLiteral.parse_action)
string_literal = pp.QuotedString("'")
literal_value = (
    numeric_literal
    | string_literal
    | kw.TRUE
    | kw.FALSE
    | kw.NULL
    | kw.CURRENT_DATE
    | kw.CURRENT_TIME
    | kw.CURRENT_TIMESTAMP
)
