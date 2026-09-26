
import runtime.base as _plcc
from runtime.base import LanguageError
from Exp import Exp



class VarExp(Exp):

    _rule_name = "VarExp"
    _fields = ["symbol"]

    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol

    def __str__(self):
        return self.symbol.lexeme


