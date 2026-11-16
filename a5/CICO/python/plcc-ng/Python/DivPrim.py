
import runtime.base as _plcc
from runtime.base import LanguageError
from Prim import Prim

from IntVal import IntVal
from runtime.base import LanguageError


class DivPrim(Prim):

    _rule_name = "DivPrim"
    _fields = []

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "/"

    def apply(self, args):
        if len(args) != 2:
            raise LanguageError("two arguments expected")
        i0 = args[0].intVal().val
        i1 = args[1].intVal().val
        if i1 == 0:
            raise LanguageError("attempt to divide by zero")
        return IntVal(int(i0 / i1))


