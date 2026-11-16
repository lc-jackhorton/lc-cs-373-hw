
import runtime.base as _plcc
from runtime.base import LanguageError
from Exp import Exp



class PrimappExp(Exp):

    _rule_name = "PrimappExp"
    _fields = ["prim", "rands"]

    def __init__(self, prim, rands):
        super().__init__()
        self.prim = prim
        self.rands = rands

    def eval(self, env):
        args = self.rands.evalRands(env)
        return self.prim.apply(args)

    def __str__(self):
        return f"{self.prim}({self.rands})"


