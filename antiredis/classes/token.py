class Token:
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def eval(self, context):
        pass

    @classmethod
    def parse_action(cls, toks):
        return toks
