import pyparsing as pp
from .token import Token
from .literal import literal_value, wildcard_all
from .identifier import col_name, func_name
from . import symbol as sym
from . import keyword as kw


class Expression(Token):
    pass


class FuncCall(Token):
    def __init__(self, func_name, args):
        super().__init__()
        self.func_name = func_name
        self.args = args

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} func_name='{self.func_name}' args='{self.args}'>"

    def eval(self, context):
        return 0

    @classmethod
    def parse_action(cls, toks):
        return FuncCall(toks[0], toks[1])


class UniaryOp(Token):
    op_map = {
        '+': lambda rhs: +rhs,
        '-': lambda rhs: -rhs,
        '~': lambda rhs: ~rhs,
    }

    def __init__(self, rhs, op):
        super().__init__()
        self.rhs = rhs
        self.op = op

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} operand='{self.rhs}' op='{self.op}'>"

    def eval(self, context):
        return UniaryOp.op_map[self.op](self.rhs.eval(context))

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

    def eval(self, context):
        return ArithOp.op_map[self.op](self.lhs.eval(context), self.rhs.eval(context))


expr = pp.Forward()

func_call = func_name + sym.LPARAM + \
    pp.Optional(pp.Group(wildcard_all | pp.delimited_list(expr))) + sym.RPARAM
func_call.set_parse_action(FuncCall.parse_action)

expr_term = (
    func_call
    | literal_value
    | col_name
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

        (pp.one_of('/ % *') | kw.NOT, BINARY,
         pp.opAssoc.LEFT, ArithOp.parse_action),

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

    exp = "(1 + sum(x, y)) * 5 / 3 - 7 % 3"
    res = expr.parse_string(exp)
    # print(res)
    print(f'{exp}\n\n{res}\n\nresult: {res[0].eval({})}')
