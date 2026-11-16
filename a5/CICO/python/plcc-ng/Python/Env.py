from Bindings import Bindings
from runtime.base import LanguageError

# Environment-related classes
#
# envRef is envVal with one level of indirection: a Binding holds a Ref
# rather than a Val, so a binding's value can be mutated in place by
# `set`. applyEnvRef is the primitive; applyEnv is derived from it.
#
# checkDuplicates returns None. That is the majority shape across the
# seven languages that use envRef, and no caller anywhere in src/ uses a
# return value from it. Do not restore the Set-returning variant that the
# old flat src/Env/envRef and src/REF/envRef carried.


class Env:

    @staticmethod
    def checkDuplicates(symbolList, msg=""):
        seen = set()
        for sym in symbolList:
            s = sym.lexeme
            if s in seen:
                raise LanguageError("duplicate ID " + s + msg)
            seen.add(s)

    @staticmethod
    def initEnv():
        from EnvNode import EnvNode
        from EnvNull import EnvNull
        return EnvNode(Bindings(), EnvNull())

    def lookup(self, sym):
        raise NotImplementedError

    def applyEnvRef(self, sym):
        raise NotImplementedError

    def applyEnv(self, sym):
        return self.applyEnvRef(sym).deRef()

    def extendEnvRef(self, bindings):
        from EnvNode import EnvNode
        return EnvNode(bindings, self)

    def add(self, binding):
        raise NotImplementedError