
import runtime.base as _plcc
from runtime.base import LanguageError
from Prim import Prim

from IntVal import IntVal
from runtime.base import LanguageError


class ZeropPrim(Prim):

    _rule_name = "ZeropPrim"
    _fields = []

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "zero?"

    def apply(self, args):
        if len(args) != 1:
            raise LanguageError("one argument expected")
        i0 = args[0].intVal().val
        return IntVal(1 if i0 == 0 else 0)


