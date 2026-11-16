
import runtime.base as _plcc
from runtime.base import LanguageError
from Prim import Prim

from IntVal import IntVal
from runtime.base import LanguageError


class MulPrim(Prim):

    _rule_name = "MulPrim"
    _fields = []

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "*"

    def apply(self, args):
        if len(args) != 2:
            raise LanguageError("two arguments expected")
        i0 = args[0].intVal().val
        i1 = args[1].intVal().val
        return IntVal(i0 * i1)


