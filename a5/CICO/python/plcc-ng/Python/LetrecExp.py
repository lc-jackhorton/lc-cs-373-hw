
import runtime.base as _plcc
from runtime.base import LanguageError
from Exp import Exp



class LetrecExp(Exp):

    _rule_name = "LetrecExp"
    _fields = ["letDecls", "exp"]

    def __init__(self, letDecls, exp):
        super().__init__()
        self.letDecls = letDecls
        self.exp = exp

    def eval(self, env):
        env = self.letDecls.addLetrecBindings(env)
        return self.exp.eval(env)

    def __str__(self):
        return " ...LetrecExp... "


