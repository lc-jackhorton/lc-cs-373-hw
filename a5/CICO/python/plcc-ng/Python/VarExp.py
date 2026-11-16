
import runtime.base as _plcc
from runtime.base import LanguageError
from Exp import Exp

from VarRef import VarRef


class VarExp(Exp):

    _rule_name = "VarExp"
    _fields = ["symbol"]

    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol

    def eval(self, env):
        return env.applyEnv(self.symbol.lexeme)

    def evalRef(self, env):
        return VarRef(env.applyEnvRef(self.symbol.lexeme))

    def __str__(self):
        return self.symbol.lexeme


