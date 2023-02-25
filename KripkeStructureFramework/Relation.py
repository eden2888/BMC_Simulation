class Relation:
    def __init__(self, fromNode, toNode):
        self._fromNode = fromNode
        self._toNode = toNode

    def __eq__(self, other):
        if not isinstance(other, Relation):
            return False
        return (self._fromNode == other._fromNode) and (self._toNode == other._toNode)

    def __hash__(self):
        return hash(self._fromNode)+hash(self._toNode)
