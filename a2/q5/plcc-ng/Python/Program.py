
import runtime.base as _plcc
from runtime.base import LanguageError
from _Start import _Start



class Program(_Start):

    _rule_name = "Program"
    _fields = ["exp"]

    def __init__(self, exp):
        super().__init__()
        self.exp = exp

    def _run(self):
        return str(self.exp)


