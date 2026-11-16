from Bindings import Bindings
from Val import Val
from runtime.base import LanguageError


class ProcVal(Val):

    def __init__(self, formals, body, env):
        self.formals = formals
        self.body = body
        self.env = env

    def apply(self, args, env):
        if len(self.formals.symbolList) != len(args):
            raise LanguageError("formals/args number mismatch")
        bindings = Bindings(self.formals.symbolList, args)
        nenv = self.env.extendEnvRef(bindings)
        result = self.body.eval(nenv)

        for ref in args: 
            ref.copyOut()

        return result

    def __str__(self):
        return "proc"