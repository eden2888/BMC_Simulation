from z3 import *


class T_Matrix:
    '''
    A class that holds a matrix of boolean variables for Z3 library use.
    '''
    def __init__(self, n, m):
        self.m = m
        self.n = n
        self.lst = []
        for i in range(n):
            self.lst.append(BoolVector('T' + str(i), m))

    def __getitem__(self, item):
        return self.lst[item]

    def __setitem__(self, key, value):
        (self.lst[key[0]])[key[1]] = value
