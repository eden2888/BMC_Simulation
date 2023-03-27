import math
from Utils import StateRef
from Utils.StateRef import StateRef
import z3
from z3 import *

from Utils.T_Matrix import T_Matrix


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
        i_formula = None
        i_formula_lst = []
        num_of_nodes = system.get_size()
        num_of_bits = round(math.log(num_of_nodes, 2))
        indexes = BoolVector(prefix, num_of_bits)
        initial_nodes = system.get_initials()
        # if no initial nodes, return false:
        if len(initial_nodes) == 0:
            return False
        # create state_ref for each node:
        for node in initial_nodes:
            node_expr_lst = []
            true_bools = SystemUtils.decimalToPaddedBinary(node.index, num_of_bits)
            for i in range(num_of_bits):
                if true_bools[i] == '0':
                    index_expr = Not(indexes[i])
                else:
                    index_expr = indexes[i]

                node_expr_lst.append(index_expr)
            if len(node_expr_lst) > 1:
                i_formula_lst.append(And(node_expr_lst))
            else:
                i_formula_lst.append(node_expr_lst[0])
        i_formula = Or(i_formula_lst)
        return i_formula

    @staticmethod
    def get_q_formula(system):
        return 0

    @staticmethod
    def get_r_formula(system):
        return 0

    @staticmethod
    def create_alpha_1(system1, system2, T):
        # T = T_Matrix(system1.get_size(), system2.get_size())
        alpha1 = None
        alpha1_expr_lst = []
        for q in system1.get_initials():
            initial_row = []
            for t in system2.get_initials():
                initial_row.append(T[q.index][t.index])
            alpha1_expr_lst.append(Or(initial_row))
        alpha1 = And(alpha1_expr_lst)
        return alpha1

    @staticmethod
    def create_alpha_2(system1, system2, T):
        exp_lst = []
        for i in range(system1.get_size()):
            for j in range(system2.get_size()):
                expr = Implies(T[i][j], SystemUtils.equals(system1.get_nodes()[i], system2.get_nodes()[j]))
                exp_lst.append(expr)
        return And(exp_lst)

    @staticmethod
    def equals(node1, node2, eq_method=None):
        if eq_method is None:
            return node1 == node2
        return eq_method(node1, node2)
