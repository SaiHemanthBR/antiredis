import time
import pyparsing as pp
from .token import Token
from .literal import literal_value, wildcard_all
from .identifier import col_name, func_name
from .context import base_context
from . import symbol as sym
from . import keyword as kw


pp.ParserElement.enable_packrat()

class Expression(Token):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} expr='{self.expr}'>"

    def eval(self, context):
        return  self.expr.eval(context)

    @classmethod
    def parse_action(cls, toks):
        return Expression(toks[0])


class BoolExpression(Expression):
    def eval(self, context):
        return bool(super().eval(context))


class FuncCall(Token):
    def __init__(self, func_name, args):
        super().__init__()
        self.func_name = func_name
        self.args = args

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} func_name='{self.func_name}' args='{self.args}'>"

    def eval(self, context):
        args = [args.eval(context) for args in self.args]
        return context['global_funcs'][self.func_name.eval(context)].eval(context, args)

    @classmethod
    def parse_action(cls, toks):
        return FuncCall(toks[0], toks[1])


class UnaryOp(Token):
    op_map = {
        '+': lambda rhs: +rhs,
        '-': lambda rhs: -rhs,
        '~': lambda rhs: ~rhs,
        '!': lambda rhs: not rhs,
        'NOT': lambda rhs: not rhs,
    }

    def __init__(self, rhs, op):
        super().__init__()
        self.rhs = rhs
        self.op = op

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} operand='{self.rhs}' op='{self.op}'>"

    def eval(self, context):
        return UnaryOp.op_map[self.op](self.rhs.eval(context))

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


class TernaryOp(Token):
    def __init__(self, lhs, mhs, rhs, op):
        super().__init__()
        self.lhs = lhs
        self.mhs = mhs
        self.rhs = rhs
        self.op = op

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} lhs='{self.lhs}' mhs='{self.mhs}' rhs='{self.rhs}' op='{self.op}'>"

    @classmethod
    def parse_action(cls, toks):
        return cls(toks[0][0], toks[0][2], toks[0][4], f'{toks[0][1]}_{toks[0][3]}')


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


class BinaryBitwiseOp(BinaryOp):
    op_map = {
        '<<': lambda lhs, rhs: lhs << rhs,
        '>>': lambda lhs, rhs: lhs >> rhs,
        '&': lambda lhs, rhs: lhs & rhs,
        '|': lambda lhs, rhs: lhs | rhs,
        '^': lambda lhs, rhs: lhs ^ rhs,
    }

    def eval(self, context):
        return BinaryBitwiseOp.op_map[self.op](self.lhs.eval(context), self.rhs.eval(context))


class BinaryComparisonOp(BinaryOp):
    op_map = {
        '=': lambda lhs, rhs: lhs == rhs,
        '==': lambda lhs, rhs: lhs == rhs,
        '>=': lambda lhs, rhs: lhs >= rhs,
        '>': lambda lhs, rhs: lhs > rhs,
        '<=': lambda lhs, rhs: lhs <= rhs,
        '<': lambda lhs, rhs: lhs < rhs,
        '<>': lambda lhs, rhs: lhs != rhs,
        '!=': lambda lhs, rhs: lhs != rhs,
    }

    def eval(self, context):
        return BinaryComparisonOp.op_map[self.op](self.lhs.eval(context), self.rhs.eval(context))


class TernaryComparisonOp(TernaryOp):
    op_map = {
        'BETWEEN_AND': lambda lhs, mhs, rhs: mhs <= lhs <= rhs,
        'NOT_BETWEEN_AND': lambda lhs, mhs, rhs: not(mhs <= lhs <= rhs),
    }

    def eval(self, context):
        return TernaryComparisonOp.op_map[self.op](self.lhs.eval(context), self.mhs.eval(context), self.rhs.eval(context))


class BinaryLogicalOp(BinaryOp):
    op_map = {
        'AND': lambda lhs, rhs: lhs and rhs,
        '&&': lambda lhs, rhs: lhs and rhs,
        'OR': lambda lhs, rhs: lhs or rhs,
        '||': lambda lhs, rhs: lhs or rhs,
        'XOR': lambda lhs, rhs: bool(lhs) != bool(rhs),
    }

    def eval(self, context):
        return BinaryLogicalOp.op_map[self.op](self.lhs.eval(context), self.rhs.eval(context))


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
NOT_BETWEEN = (kw.NOT + kw.BETWEEN).set_parse_action(lambda toks: f'{toks[0]}_{toks[1]}')

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

where_expr = expr().set_parse_action(BoolExpression.parse_action)
having_expr = expr().set_parse_action(BoolExpression.parse_action)

if __name__ == '__main__':
    exp = "CURRENT_DATE == date('2022-01-24')"

    then = time.time()
    res = where_expr.parse_string(exp)
    now = time.time()
    # print(res, now - then)
    print(f'{exp}\n\n{res[0]}\n\nResult: {res[0].eval(base_context)}\n\nTime: {now - then}')
