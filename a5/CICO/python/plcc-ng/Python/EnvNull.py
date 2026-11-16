from Env import Env
from runtime.base import LanguageError


class EnvNull(Env):

    def applyEnvRef(self, sym):
        raise LanguageError("no binding for " + sym)

    def lookup(self, sym):
        return None

    def add(self, binding):
        raise LanguageError("no bindings to add to")

    def __str__(self):
        return "\n"