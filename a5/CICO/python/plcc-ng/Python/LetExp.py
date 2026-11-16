
import runtime.base as _plcc
from runtime.base import LanguageError
from Exp import Exp



class LetExp(Exp):

    _rule_name = "LetExp"
    _fields = ["letDecls", "exp"]

    def __init__(self, letDecls, exp):
        super().__init__()
        self.letDecls = letDecls
        self.exp = exp

    def eval(self, env):
        nenv = self.letDecls.addBindings(env)
        return self.exp.eval(nenv)

    def __str__(self):
        return " ...LetExp... "


