
import runtime.base as _plcc
from runtime.base import LanguageError



class Classes(_plcc.Node):

    _rule_name = "Classes"
    _fields = ["c1", "c2", "c3"]

    def __init__(self, c1, c2, c3):
        super().__init__()
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3


