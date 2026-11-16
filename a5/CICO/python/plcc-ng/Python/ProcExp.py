
import runtime.base as _plcc
from runtime.base import LanguageError
from Exp import Exp



class ProcExp(Exp):

    _rule_name = "ProcExp"
    _fields = ["proc"]

    def __init__(self, proc):
        super().__init__()
        self.proc = proc

    def eval(self, env):
        return self.proc.makeClosure(env)

    def __str__(self):
        return " ...ProcExp... "


