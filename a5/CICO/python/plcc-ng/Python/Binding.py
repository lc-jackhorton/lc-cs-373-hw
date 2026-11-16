class Binding:

    def __init__(self, id, ref):
        self.id = id
        self.ref = ref

    def __str__(self):
        return f"[{self.id}:{self.ref.deRef()}]"