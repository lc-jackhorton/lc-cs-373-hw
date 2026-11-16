class Ref:

    @staticmethod
    def valsToRefs(valList):
        from ValRef import ValRef
        return [ValRef(v) for v in valList]

    def deRef(self):
        raise NotImplementedError

    def setRef(self, v):
        raise NotImplementedError

    def copyOut(self):
        pass