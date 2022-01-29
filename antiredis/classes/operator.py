from .token import Token


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
