
import runtime.base as _plcc
from runtime.base import LanguageError
from Program import Program

from Binding import Binding
from ValRef import ValRef


class Define(Program):

    _rule_name = "Define"
    _fields = ["symbol", "exp"]

    def __init__(self, symbol, exp):
        super().__init__()
        self.symbol = symbol
        self.exp = exp

    def _run(self):
        env = Program.env
        s = self.symbol.lexeme
        val = self.exp.eval(env)
        ref = ValRef(val)
        b = env.lookup(s)
        if b is not None:
            b.ref = ref
        else:
            env.add(Binding(s, ref))
        return s


