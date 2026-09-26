
import runtime.base as _plcc
from runtime.base import LanguageError
from Nums import Nums



class More(Nums):

    _rule_name = "More"
    _fields = ["num", "nums"]

    def __init__(self, num, nums):
        super().__init__()
        self.num = num
        self.nums = nums

    def min(self, best):
        n = int(self.num.lexeme)
        if n < best:
            best = n
        return self.nums.min(best)


