class Node:
    '''
    This class holds a single node in a Kripke Structure
    Each node consists of a several variables:
    Index, Assignment, isInitial flag, set of relations to other nodes (set of indexes)
    and assignments for prediction variables
    '''

    def __init__(self, index, assignment="", isInitial=False, **kwargs):
        if len(kwargs) == 0:
            self.__index = index
            self.__assignment = assignment
            self.__isInitial = isInitial
            self.__relations = set()
            self.nextAssignment = ''
            self.nextNextAssignment = ''
            self.__prev_index = index
        else:
            self.__index = index
            self.__relations = set()
            for key in kwargs.keys():
                if key == 'node':
                    self.__prev_index = kwargs.get(key).index
                    self.__assignment = kwargs.get(key).assignment
                    self.__isInitial = kwargs.get(key).isInitial
                elif key == 'next':
                    self.nextAssignment = kwargs.get(key)
                elif key == 'nextNext':
                    self.nextNextAssignment = kwargs.get(key)

    def __str__(self):
        return 'index: {self.__index}, relations: {self.__relations}, isInitial: {self.__isInitial}'.format(self=self)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.assignment == other.assignment
        return False

    @property
    def prev_index(self):
        return self.__prev_index

    @prev_index.setter
    def prev_index(self, value):
        self.__prev_index == value

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
    def index(self, value):
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
