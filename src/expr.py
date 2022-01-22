import pyparsing as pp
from .token import Token
from .literal import literal_value, wildcard_all
from .identifier import col_name, func_name
from . import symbol as sym
from . import keyword as kw


class Expression(Token):
    pass


class UniaryOp(Token):
    op_map = {
        '+': lambda rhs: +rhs,
        '-': lambda rhs: -rhs,
        '~': lambda rhs: ~rhs,
    }

    def __init__(self, rhs, op) -> None:
        super().__init__()
        self.rhs = rhs
        self.op = op

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} operand='{self.rhs}' op='{self.op}'>"

    def eval(self):
        return UniaryOp.op_map[self.op](self.rhs.eval())

    @classmethod
    def parse_action(cls, toks):
        return cls(toks[0][1], toks[0][0])


class BinaryOp(Token):
    def __init__(self, lhs, rhs, op):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} lhs='{self.lhs}' rhs='{self.rhs}' op='{self.op}'>"

    @classmethod
    def parse_action(cls, toks):
        return cls(toks[0][0], toks[0][2], toks[0][1])


class ArithOp(BinaryOp):
    op_map = {
        '/': lambda lhs, rhs: lhs / rhs,
        '%': lambda lhs, rhs: lhs % rhs,
        '*': lambda lhs, rhs: lhs * rhs,
        '+': lambda lhs, rhs: lhs + rhs,
        '-': lambda lhs, rhs: lhs - rhs,
    }

    def eval(self):
        return ArithOp.op_map[self.op](self.lhs.eval(), self.rhs.eval())


expr = pp.Forward()
func_call = func_name + sym.LPARAM + \
    pp.Optional(wildcard_all | pp.delimited_list(expr)) + sym.RPARAM
expr_term = (
    literal_value
    | col_name
    | func_call
)

UNARY, BINARY, TERTIARY = 1, 2, 3

"""
+ (unary plus), - (unary minus), ~ (unary bit inversion)
*, /, DIV, %, MOD
-, +
<<, >>
&
|
= (comparison), <=>, >=, >, <=, <, <>, !=, IS, LIKE, REGEXP, IN, MEMBER OF
BETWEEN, CASE, WHEN, THEN, ELSE
!, NOT
AND, &&
^, XOR
OR, ||
"""
expr << pp.infix_notation(
    expr_term,
    [
        (pp.one_of('+ - ~') | kw.NOT, UNARY,
         pp.opAssoc.RIGHT, UniaryOp.parse_action),
        (pp.one_of('/ % *') | kw.NOT, BINARY, pp.opAssoc.LEFT, ArithOp.parse_action),
        (pp.one_of('+ -') | kw.NOT, BINARY, pp.opAssoc.LEFT, ArithOp.parse_action),
    ]
)

if __name__ == '__main__':
    # res = expr.parse_string('-5')[0]
    # print(res, res.eval())

    # res = expr.parse_string('4 * 5 + 1')[0]
    # print(res, res.eval())

    # res = expr.parse_string("1 + 4 * 5")[0]
    # print(res, res.eval())

    exp = "(1 + 4) * 5 / 3 - 7 % 3"
    res = expr.parse_string(exp)[0]
    print(f'{exp}\n\n{res}\n\nresult: {res.eval()}')
