
import runtime.base as _plcc
from runtime.base import LanguageError
from Prim import Prim



class Sub1Prim(Prim):

    _rule_name = "Sub1Prim"
    _fields = []

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "sub1"


