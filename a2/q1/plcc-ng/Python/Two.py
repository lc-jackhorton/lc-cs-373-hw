
import runtime.base as _plcc
from runtime.base import LanguageError
from Start import Start



class Two(Start):

    _rule_name = "Two"
    _fields = ["many"]

    def __init__(self, many):
        super().__init__()
        self.many = many


