from Ref import Ref


class ValRef(Ref):

    def __init__(self, val):
        self.val = val

    def deRef(self):
        return self.val

    def setRef(self, v):
        self.val = v
        return v

    def __str__(self):
        return str(self.val)