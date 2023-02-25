class Node:
    def __init__(self, index, assignment="", isInitial=False):
        self.__index = index
        self.__assignment = assignment
        self.__isInitial = isInitial

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
    