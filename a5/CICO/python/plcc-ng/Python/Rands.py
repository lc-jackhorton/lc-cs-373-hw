
import runtime.base as _plcc
from runtime.base import LanguageError



class Rands(_plcc.Node):

    _rule_name = "Rands"
    _fields = ["expList"]

    def __init__(self, expList):
        super().__init__()
        self.expList = expList

    def evalRands(self, env):
        return [e.eval(env) for e in self.expList]

    def evalRandsRef(self, env):
        return [e.evalRef(env) for e in self.expList]

    def __str__(self):
        return ",".join(str(e) for e in self.expList)


