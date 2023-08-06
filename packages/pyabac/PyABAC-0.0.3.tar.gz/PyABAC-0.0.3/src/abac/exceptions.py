class ABACError(Exception):
    pass

class DecorationError(ABACError):  # noqa: B903
    def __init__(self, func, funcname, issue):
        self.func = func
        self.funcname = funcname
        self.issue = issue
        super().__init__(issue)
