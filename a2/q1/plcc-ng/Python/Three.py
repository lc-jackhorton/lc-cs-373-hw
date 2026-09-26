
import runtime.base as _plcc
from runtime.base import LanguageError
from Start import Start



class Three(Start):

    _rule_name = "Three"
    _fields = ["classes"]

    def __init__(self, classes):
        super().__init__()
        self.classes = classes


