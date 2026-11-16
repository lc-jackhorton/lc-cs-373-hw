from Env import Env


class EnvNode(Env):

    def __init__(self, bindings, env):
        self.bindings = bindings
        self.env = env

    def lookup(self, sym):
        return self.bindings.lookup(sym)

    def applyEnvRef(self, sym):
        b = self.bindings.lookup(sym)
        if b is None:
            return self.env.applyEnvRef(sym)
        return b.ref

    def add(self, binding):
        self.bindings.add(binding)
        return self

    def __str__(self):
        return f"{self.bindings}----\n{self.env}"