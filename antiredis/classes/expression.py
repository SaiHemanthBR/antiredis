from .token import Token


class Expression(Token):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} expr='{self.expr}'>"

    def eval(self, context):
        return self.expr.eval(context)

    @classmethod
    def parse_action(cls, toks):
        return Expression(toks[0])


class BoolExpression(Expression):
    def eval(self, context):
        return bool(super().eval(context))
