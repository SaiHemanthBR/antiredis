from ..lib import time
from .function import Func


base_context = {
    'global_funcs': {
        'date': Func(time.date, 1)
    }
}
