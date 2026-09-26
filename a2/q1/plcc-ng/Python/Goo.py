
import runtime.base as _plcc
from runtime.base import LanguageError
from Blah import Blah



class Goo(Blah):

    _rule_name = "Goo"
    _fields = ["var", "silly"]

    def __init__(self, var, silly):
        super().__init__()
        self.var = var
        self.silly = silly


