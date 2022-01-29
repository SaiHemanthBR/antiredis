from .token import Token


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
