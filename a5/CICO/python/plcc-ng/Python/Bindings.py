from Binding import Binding
from runtime.base import LanguageError


class Bindings:

    def __init__(self, idList=None, refList=None):
        self.bindingList = []
        if idList is not None:
            if refList is None or len(idList) != len(refList):
                raise LanguageError("list sizes mismatch")
            for sym, r in zip(idList, refList):
                self.bindingList.append(Binding(sym.lexeme, r))

    def lookup(self, sym):
        for b in self.bindingList:
            if sym == b.id:
                return b
        return None

    def add(self, binding):
        self.bindingList.append(binding)

    def size(self):
        return len(self.bindingList)

    def __str__(self):
        s = ""
        for b in self.bindingList:
            s += f"{b}\n"
        return s