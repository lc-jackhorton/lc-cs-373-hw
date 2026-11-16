
import runtime.base as _plcc
from runtime.base import LanguageError
from Exp import Exp



class SetExp(Exp):

    _rule_name = "SetExp"
    _fields = ["symbol", "exp"]

    def __init__(self, symbol, exp):
        super().__init__()
        self.symbol = symbol
        self.exp = exp

    def eval(self, env):
        v = self.exp.eval(env)
        ref = env.applyEnvRef(self.symbol.lexeme)
        return ref.setRef(v)

    def __str__(self):
        return " ...SetExp... "


