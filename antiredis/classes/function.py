from .token import Token


class Func:
    def __init__(self, fn, argc):
        self.fn = fn
        self.argc = argc

    def eval(self, context, argv):
        if len(argv) != self.argc:
            raise Exception(f'Expected {self.argc}, but got {len(argv)}')
        return self.fn(*argv)


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
