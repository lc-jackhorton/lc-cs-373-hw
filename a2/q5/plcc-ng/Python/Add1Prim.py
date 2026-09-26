
import runtime.base as _plcc
from runtime.base import LanguageError
from Prim import Prim



class Add1Prim(Prim):

    _rule_name = "Add1Prim"
    _fields = []

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "add1"


