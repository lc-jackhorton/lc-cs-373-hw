
import runtime.base as _plcc
from runtime.base import LanguageError

from ValRef import ValRef


class Exp(_plcc.Node):

    _rule_name = "Exp"
    _fields = []

    def __init__(self):
        super().__init__()

    def evalRef(self, env):
        return ValRef(self.eval(env))


