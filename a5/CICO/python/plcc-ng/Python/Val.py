from runtime.base import LanguageError


class Val:

    # Some Vals can be applied to a list of arguments (e.g. a ProcVal).
    # Like the evaluation of an expression, the application of a Val takes
    # place in the context of an environment, which arrives as the second
    # parameter. An applied Val may use or ignore that environment as its
    # own semantics require.
    def apply(self, args, env):
        raise LanguageError(f"Cannot apply {self}")

    def isTrue(self):
        return True

    def intVal(self):
        raise LanguageError(f"{self}: not an Int")