import pyparsing as pp
from pyparsing import pyparsing_common as ppc
from datetime import datetime, date
import time
from .token import Token
from . import symbol as sym
from . import keyword as kw


class WildcardAll(Token):
    pass


class Literal(Token):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} value='{self.value}'>"

    def eval(self, context):
        return self.value

    @classmethod
    def parse_action(cls, toks):
        return cls(toks[0])


wildcard_all = pp.Literal('*')
wildcard_all.set_parse_action(WildcardAll.parse_action)

numeric_literal = ppc.number.set_parse_action(Literal.parse_action)
string_literal = pp.QuotedString("'").set_parse_action(Literal.parse_action)
bool_literal = (kw.TRUE | kw.FALSE).set_parse_action(Literal.parse_action)
null_literal = (kw.NULL).set_parse_action(lambda: Literal(None))

current_date_literal = (kw.CURRENT_DATE).set_parse_action(
    lambda: Literal(date.today()))
current_time_literal = (kw.CURRENT_TIME).set_parse_action(
    lambda: Literal(datetime.now().time().replace(microsecond=0)))
current_timestamp_literal = (kw.CURRENT_TIMESTAMP).set_parse_action(
    lambda: Literal(datetime.now().replace(microsecond=0)))

literal_value = (
    numeric_literal
    | string_literal
    | bool_literal
    | null_literal
    | current_date_literal
    | current_time_literal
    | current_timestamp_literal
)
