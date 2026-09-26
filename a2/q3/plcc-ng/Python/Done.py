
import runtime.base as _plcc
from runtime.base import LanguageError
from Nums import Nums



class Done(Nums):

    _rule_name = "Done"
    _fields = []

    def __init__(self):
        super().__init__()

    def sum(self, total):
        return total


