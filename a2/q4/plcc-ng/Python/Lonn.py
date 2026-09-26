
import runtime.base as _plcc
from runtime.base import LanguageError
from _Start import _Start



class Lonn(_Start):

    _rule_name = "Lonn"
    _fields = ["num", "nums"]

    def __init__(self, num, nums):
        super().__init__()
        self.num = num
        self.nums = nums

    def _run(self):
        first = int(self.num.lexeme)
        return str(self.nums.min(first))


