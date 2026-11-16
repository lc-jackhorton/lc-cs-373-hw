
import runtime.base as _plcc
from runtime.base import LanguageError
from Exp import Exp

from IntVal import IntVal


class LitExp(Exp):

    _rule_name = "LitExp"
    _fields = ["lit"]

    def __init__(self, lit):
        super().__init__()
        self.lit = lit

    def eval(self, env):
        return IntVal(self.lit.lexeme)

    def __str__(self):
        return self.lit.lexeme


