class Node:
    def __init__(self, index, assignment="", isInitial=False):
        self.__index = index
        self.__assignment = assignment
        self.__isInitial = isInitial
        self.__relations = set()
        self.nextAssignment = ''
        self.nextNextAssignment = ''

    def __init__(self, node, next, nextNext):
        self.__index = node.index
        self.__assignment = node.assignment
        self.__isInitial = node.isInitial
        self.__relations = set()
        self.nextAssignment = next
        self.nextNextAssignment = nextNext

    def __str__(self):
        return 'index: {self.__index}, relations: {self.__relations}, isInitial: {self.__isInitial}'.format(self=self)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.assignment == other.assignment
        return False

    @property
    def relations(self):
        return self.__relations

    @relations.setter
    def relations(self, value):
        self.__relations = value

    def add_relation(self, index):
        self.__relations.add(index)

    @property
    def index(self):
        return self.__index

    @index.setter
    def x(self, value):
        self.__index = value

    @property
    def assignment(self):
        return self.__assignment

    @assignment.setter
    def assignment(self, value):
        self.__assignment = value

    @property
    def isInitial(self):
        return self.__isInitial

    @isInitial.setter
    def isInitial(self, value):
        self.__isInitial = value
