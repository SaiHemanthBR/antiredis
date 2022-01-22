class Token:
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    @classmethod
    def parse_action(cls):
        return cls()
