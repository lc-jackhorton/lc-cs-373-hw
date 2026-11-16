
import runtime.base as _plcc
from runtime.base import LanguageError



class SeqExps(_plcc.Node):

    _rule_name = "SeqExps"
    _fields = ["expList"]

    def __init__(self, expList):
        super().__init__()
        self.expList = expList


