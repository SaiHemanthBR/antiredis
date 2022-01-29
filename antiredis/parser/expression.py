import time
import pyparsing as pp
from ..classes.expression import Expression, BoolExpression
from ..classes.function import FuncCall
from ..classes.operator import UnaryOp, BinaryBitwiseOp, ArithOp, BinaryComparisonOp, TernaryComparisonOp, BinaryLogicalOp
from .literal import literal_value, wildcard_all
from .identifier import col_name, func_name
from . import symbol as sym
from . import keyword as kw


pp.ParserElement.enable_packrat()

expr = pp.Forward()
expr.set_parse_action(Expression.parse_action)

func_call = func_name + sym.LPARAM + \
    pp.Optional(pp.Group(wildcard_all | pp.delimited_list(expr))) + sym.RPARAM
func_call.set_parse_action(FuncCall.parse_action)

expr_term = (
    literal_value
    | func_call
    | col_name
)

UNARY, BINARY, TERNARY = 1, 2, 3

"""
Operator Precedence:
===============================================================================================
+ (unary plus), - (unary minus), ~ (unary bit inversion)
^
*, /, %
-, +
<<, >>
&
|
= (comparison), >=, >, <=, <, <>, != (add support for <=>, IS, LIKE, REGEXP, IN, MEMBER OF)
BETWEEN (add support for CASE, WHEN, THEN, ELSE)
!, NOT
AND, &&
XOR
OR, ||
"""
NOT_BETWEEN = (
    kw.NOT + kw.BETWEEN).set_parse_action(lambda toks: f'{toks[0]}_{toks[1]}')

expr << pp.infix_notation(
    expr_term,
    [
        (pp.one_of('+ - ~'), UNARY,
         pp.opAssoc.RIGHT, UnaryOp.parse_action),

        (pp.one_of('^'), BINARY,
         pp.opAssoc.LEFT, BinaryBitwiseOp.parse_action),

        (pp.one_of('/ % *'), BINARY, pp.opAssoc.LEFT, ArithOp.parse_action),
        (pp.one_of('+ -'), BINARY, pp.opAssoc.LEFT, ArithOp.parse_action),

        (pp.one_of('<< >>'), BINARY, pp.opAssoc.LEFT, BinaryBitwiseOp.parse_action),
        (pp.one_of('&'), BINARY, pp.opAssoc.LEFT, BinaryBitwiseOp.parse_action),
        (pp.one_of('|'), BINARY, pp.opAssoc.LEFT, BinaryBitwiseOp.parse_action),

        (pp.one_of('= == >= > <= < <> !='), BINARY,
         pp.opAssoc.LEFT, BinaryComparisonOp.parse_action),

        ((kw.BETWEEN | NOT_BETWEEN, kw.AND), TERNARY, pp.opAssoc.LEFT,
         TernaryComparisonOp.parse_action),

        (kw.NOT | '!', UNARY, pp.opAssoc.RIGHT, UnaryOp.parse_action),

        (kw.AND | '&&', BINARY, pp.opAssoc.LEFT, BinaryLogicalOp.parse_action),
        (kw.XOR, BINARY, pp.opAssoc.LEFT, BinaryLogicalOp.parse_action),
        (kw.OR | '||', BINARY, pp.opAssoc.LEFT, BinaryLogicalOp.parse_action),
    ]
)

bool_expr = expr().set_parse_action(BoolExpression.parse_action)

if __name__ == '__main__':
    from ..classes.context import base_context

    exp = "CURRENT_DATE == date('2022-01-24')"

    then = time.time()
    res = expr.parse_string(exp)
    now = time.time()
    # print(res, now - then)
    print(
        f'{exp}\n\n{res[0]}\n\nResult: {res[0].eval(base_context)}\n\nTime: {now - then}')
