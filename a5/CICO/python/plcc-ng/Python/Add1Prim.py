
import runtime.base as _plcc
from runtime.base import LanguageError
from Prim import Prim

from IntVal import IntVal
from runtime.base import LanguageError


class Add1Prim(Prim):

    _rule_name = "Add1Prim"
    _fields = []

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "add1"

    def apply(self, args):
        if len(args) != 1:
            raise LanguageError("one argument expected")
        i0 = args[0].intVal().val
        return IntVal(i0 + 1)


