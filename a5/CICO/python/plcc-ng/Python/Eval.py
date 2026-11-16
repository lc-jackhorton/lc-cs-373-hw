
import runtime.base as _plcc
from runtime.base import LanguageError
from Program import Program



class Eval(Program):

    _rule_name = "Eval"
    _fields = ["exp"]

    def __init__(self, exp):
        super().__init__()
        self.exp = exp

    def _run(self):
        return str(self.exp.eval(Program.env))


