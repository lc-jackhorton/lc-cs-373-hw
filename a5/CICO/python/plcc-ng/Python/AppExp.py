
import runtime.base as _plcc
from runtime.base import LanguageError
from Exp import Exp



class AppExp(Exp):

    _rule_name = "AppExp"
    _fields = ["exp", "rands"]

    def __init__(self, exp, rands):
        super().__init__()
        self.exp = exp
        self.rands = rands

    def eval(self, env):
        v = self.exp.eval(env)
        args = self.rands.evalRandsRef(env)
        return v.apply(args, env)

    def __str__(self):
        return " ...AppExp... "


