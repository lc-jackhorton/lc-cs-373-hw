
import runtime.base as _plcc
from runtime.base import LanguageError
from Exp import Exp



class SeqExp(Exp):

    _rule_name = "SeqExp"
    _fields = ["exp", "seqExps"]

    def __init__(self, exp, seqExps):
        super().__init__()
        self.exp = exp
        self.seqExps = seqExps

    def eval(self, env):
        v = self.exp.eval(env)
        for e in self.seqExps.expList:
            v = e.eval(env)
        return v

    def __str__(self):
        return " ...SeqExp... "


