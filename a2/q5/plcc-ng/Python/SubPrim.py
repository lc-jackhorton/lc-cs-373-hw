
import runtime.base as _plcc
from runtime.base import LanguageError
from Prim import Prim



class SubPrim(Prim):

    _rule_name = "SubPrim"
    _fields = []

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "-"


