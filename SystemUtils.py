import math
import Utils.StateRef
import z3
from z3 import *


class SystemUtils:
    """
    This class offers several static methods that returns certain data on different systems (Kripke Structures)
    """
    @staticmethod
    def decimalToPaddedBinary(n, total_len):
        not_padded = bin(n).replace("0b", "")
        padded = ('0' * (total_len - len(not_padded))) + not_padded
        return padded

    @staticmethod
    def get_i_formula(system, prefix):
        i_formula = Or()
        # i_formula = and(state_refs)
        num_of_nodes = system.get_size()
        num_of_bits = int(math.log(num_of_nodes, 2))
        indexes = BoolVector(prefix, num_of_bits)
        initial_nodes = system.get_initials()
        # create state_ref for each node:
        for node in initial_nodes:
            true_bools = SystemUtils.decimalToPaddedBinary(node.index, num_of_bits)
            for i in range(0,num_of_bits):
                index_expr = indexes[i] # current bit boolean expression
                if true_bools[i] == '0':
                    index_expr = Not(indexes[i]) # if bit is 0, add index as Not(index)
                expr = And(expr, index_expr)
            #end node's index for
            i_formula = Or(i_formula, expr)
        return i_formula


    @staticmethod
    def get_q_formula(system):


    @staticmethod
    def get_r_formula(system):

