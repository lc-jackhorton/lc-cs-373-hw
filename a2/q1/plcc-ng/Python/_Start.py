import runtime.base as _plcc


class _Start(_plcc.Node):
    def _run(self):
        return str(self)
