
import runtime.base as _plcc
from runtime.base import LanguageError
from Start import Start



class One(Start):

    _rule_name = "One"
    _fields = ["blah"]

    def __init__(self, blah):
        super().__init__()
        self.blah = blah


