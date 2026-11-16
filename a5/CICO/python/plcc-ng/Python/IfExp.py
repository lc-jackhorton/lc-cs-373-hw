
import runtime.base as _plcc
from runtime.base import LanguageError
from Exp import Exp



class IfExp(Exp):

    _rule_name = "IfExp"
    _fields = ["testExp", "trueExp", "falseExp"]

    def __init__(self, testExp, trueExp, falseExp):
        super().__init__()
        self.testExp = testExp
        self.trueExp = trueExp
        self.falseExp = falseExp

    def eval(self, env):
        if self.testExp.eval(env).isTrue():
            return self.trueExp.eval(env)
        else:
            return self.falseExp.eval(env)

    def __str__(self):
        return f"if {self.testExp} then {self.trueExp} else {self.falseExp}"


