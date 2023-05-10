import math
import jsonpickle
from datetime import date
from KripkeStructureFramework.KripkeStructure import KripkeStructure
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
    def create_alpha_3(system1, system2, T):
        exp_lst = []
        for i in range(system1.get_size()):
            for j in range(system2.get_size()):
                node1 = system1.get_nodes()[i]
                node2 = system2.get_nodes()[j]
                expr = Implies(T[i][j], SystemUtils.create_inner_alpha_3(node1, node2, T))
                exp_lst.append(expr)
        return And(exp_lst)

    @staticmethod
    def create_inner_alpha_3(node1, node2, T):
        exp_lst = []
        for child1 in node1.relations:
            node_lst = []
            for child2 in node2.relations:
                node_lst.append(T[child1][child2])
            exp_lst.append(Or(node_lst))
        return And(exp_lst)

    @staticmethod
    def equals(node1, node2, eq_method=None):
        if eq_method is None:
            return node1 == node2
        return eq_method(node1, node2)

    @staticmethod
    def save_system(system, path):
        nodes = system.get_nodes()
        system_json = jsonpickle.encode(nodes)
        with open(path, "w") as outfile:
            outfile.write(system_json)

    @staticmethod
    def load_system(path):
        try:
            system_json = open(path)
            file_data = system_json.read()
            decoded = jsonpickle.decode(file_data)
            loaded_system = KripkeStructure(decoded)
            return loaded_system
        except:
            return None

    @staticmethod
    def get_all_systems_from_path():
        return [pos_json for pos_json in os.listdir('c:\BMC_Systems') if pos_json.endswith('.json')]

    @staticmethod
    def get_relations_list(system):
        relations_list = []
        for node in system.get_nodes():
            for relation in node.relations:
                relations_list.append((node.index, relation))
        return relations_list

    @staticmethod
    def get_node_names_dictionary(system):
        names_dict = {}
        for node in system.get_nodes():
            if "" == node.assignment:
                names_dict[node.index] = str(node.index)
            else:
                names_dict[node.index] = str(node.index) + ', ' + node.assignment
        return names_dict

    @staticmethod
    def get_node_color_list(system):
        colors_lst = []
        for node in system.get_nodes():
            if node.isInitial:
                colors_lst.append('#0080ff')
            else:
                colors_lst.append('#CCCCFF')
        return colors_lst

    @staticmethod
    def check_simulation(sys1, sys2):
        T = T_Matrix(sys1.get_size(), sys2.get_size())
        i_1 = SystemUtils.get_i_formula(sys1, 'x')
        i_2 = SystemUtils.get_i_formula(sys2, 'y')
        c = i_1.children()
        # create T[m,n]:
        alpha1 = SystemUtils.create_alpha_1(sys1, sys2, T)
        alpha2 = SystemUtils.create_alpha_2(sys1, sys2, T)
        alpha3 = SystemUtils.create_alpha_3(sys1, sys2, T)
        s = Solver()
        s.add(alpha1)
        s.add(alpha2)
        s.add(alpha3)
        return s


