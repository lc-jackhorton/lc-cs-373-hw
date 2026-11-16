
import runtime.base as _plcc
from runtime.base import LanguageError

from Env import Env


class Formals(_plcc.Node):

    _rule_name = "Formals"
    _fields = ["symbolList"]

    def __init__(self, symbolList):
        super().__init__()
        self.symbolList = symbolList
        Env.checkDuplicates(self.symbolList, " in proc formals")


