
import runtime.base as _plcc
from runtime.base import LanguageError
from Prim import Prim



class AddPrim(Prim):

    _rule_name = "AddPrim"
    _fields = []

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "+"


