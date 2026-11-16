from ValRef import ValRef


class VarRef(ValRef):

    def __init__(self, ref):
        super().__init__(ref.deRef())   # copy in: a new ref holding a copy
        self.ref = ref                  # the variable's own ref, kept for later

    def copyOut(self):
        # Put this ref's value back into the variable's own ref.
        self.ref.setRef(self.deRef())