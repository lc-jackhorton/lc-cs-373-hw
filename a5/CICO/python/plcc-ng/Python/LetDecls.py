
import runtime.base as _plcc
from runtime.base import LanguageError

from Env import Env
from Binding import Binding
from Bindings import Bindings
from Ref import Ref
from ValRef import ValRef


class LetDecls(_plcc.Node):

    _rule_name = "LetDecls"
    _fields = ["symbolList", "expList"]

    def __init__(self, symbolList, expList):
        super().__init__()
        self.symbolList = symbolList
        self.expList = expList
        Env.checkDuplicates(self.symbolList, " in let/letrec LHS identifiers")

    def addBindings(self, env):
        valList = [e.eval(env) for e in self.expList]
        refList = Ref.valsToRefs(valList)
        bindings = Bindings(self.symbolList, refList)
        return env.extendEnvRef(bindings)

    def addLetrecBindings(self, env):
        env = env.extendEnvRef(Bindings())
        for sym, e in zip(self.symbolList, self.expList):
            val = e.eval(env)
            env.add(Binding(sym.lexeme, ValRef(val)))
        return env

    def __str__(self):
        return " ...LetDecls... "


