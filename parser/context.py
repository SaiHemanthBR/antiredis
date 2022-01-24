from datetime import datetime

def date(str):
    return datetime.strptime(str, '%Y-%m-%d').date()

class Func:
    def __init__(self, fn, argc):
        self.fn = fn
        self.argc = argc

    def eval(self, context, argv):
        if len(argv) != self.argc:
            raise Exception(f'Expected {self.argc}, but got {len(argv)}')
        return self.fn(*argv)


base_context = {
    'global_funcs': {
        'date': Func(date, 1)
    }
}
