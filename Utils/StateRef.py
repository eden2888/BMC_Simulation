from z3 import BoolRef


class StateRef(BoolRef):

    def __init__(self, expr, state_id=0, ctx=None):
        BoolRef.__init__(self, expr.ast, ctx)
        self.state_id = state_id


