import math
from Utils import StateRef
from Utils.StateRef import StateRef
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
        i_formula_flag = 0
        node_expr_flag = 0
        # i_formula = and(state_refs)
        num_of_nodes = system.get_size()
        num_of_bits = int(math.log(num_of_nodes, 2))
        indexes = BoolVector(prefix, num_of_bits)
        initial_nodes = system.get_initials()
        # create state_ref for each node:
        for node in initial_nodes:
            node_expr_flag = 0
            node_expr = None
            true_bools = SystemUtils.decimalToPaddedBinary(node.index, num_of_bits)
            node_expr = 0 #StateRef(And([]), node.index)
            for i in range(num_of_bits):
                if true_bools[i] == '0':
                    index_expr = Not(indexes[i])
                else:
                    index_expr = indexes[i]

                if node_expr_flag == 0:
                    node_expr = index_expr
                    node_expr_flag = 1
                else:
                    node_expr = And([node_expr, index_expr])
                #node_expr = And([node_expr, index_expr])
            if i_formula_flag == 0:
                i_formula = node_expr
                i_formula_flag = 1
            else:
                i_formula = Or([i_formula, node_expr])

        return i_formula

    @staticmethod
    def get_q_formula(system):
        return 0

    @staticmethod
    def get_r_formula(system):
        return 0

