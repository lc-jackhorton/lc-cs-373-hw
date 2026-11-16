from Val import Val


class IntVal(Val):

    def __init__(self, val):
        self.val = int(val)

    def intVal(self):
        return self

    def __str__(self):
        return str(self.val)

    def isTrue(self):
        return self.val != 0