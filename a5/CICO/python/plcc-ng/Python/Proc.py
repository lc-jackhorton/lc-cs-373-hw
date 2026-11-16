
import runtime.base as _plcc
from runtime.base import LanguageError

from ProcVal import ProcVal


class Proc(_plcc.Node):

    _rule_name = "Proc"
    _fields = ["formals", "exp"]

    def __init__(self, formals, exp):
        super().__init__()
        self.formals = formals
        self.exp = exp

    def makeClosure(self, env):
        return ProcVal(self.formals, self.exp, env)


