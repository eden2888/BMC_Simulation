import jsonpickle
from KripkeStructureFramework.KripkeStructure import KripkeStructure
from KripkeStructureFramework.Node import Node
from Utils import VisualUtils
from z3 import *
from Utils.T_Matrix import T_Matrix

NEXT_0_0_OFFSET = 0
NEXT_0_1_OFFSET = 1
NEXT_1_0_OFFSET = 2
NEXT_1_1_OFFSET = 3


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
        # if no systems/path, create defaults:
        if not os.path.exists("c:\BMC_Systems"):
            os.mkdir("c:\BMC_Systems")
        VisualUtils.store_test_systems()
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
        # create T[m,n]:
        alpha1 = SystemUtils.create_alpha_1(sys1, sys2, T)
        alpha2 = SystemUtils.create_alpha_2(sys1, sys2, T)
        alpha3 = SystemUtils.create_alpha_3(sys1, sys2, T)
        s = Solver()
        # s.add(alpha1)
        # s.add(alpha2)
        s.add(alpha3)
        return s

    @staticmethod
    def create_predictive_kripke_structure(system):
        predictive_nodes = []
        i = 0

        # Create Nodes:
        for node in system.get_nodes():
            dupe_1 = Node(i, node=node, next=0, nextNext=0)
            dupe_2 = Node(i + 1, node=node, next=0, nextNext=1)
            dupe_3 = Node(i + 2, node=node, next=1, nextNext=0)
            dupe_4 = Node(i + 3, node=node, next=1, nextNext=1)
            predictive_nodes.extend([dupe_1, dupe_2, dupe_3, dupe_4])
            i += 4

        # Create Relations
        original_nodes = system.get_nodes()
        for i in range(len(predictive_nodes)):
            node = predictive_nodes[i]
            original_node = original_nodes[node.prev_index]
            for relation in original_node.relations:
                related_node = original_nodes[relation]
                has_assignment = 0 if related_node.assignment == '' else 1
                if node.nextAssignment == has_assignment and node.nextNextAssignment == 1:
                    node.relations.add(related_node.index * 4 + NEXT_1_0_OFFSET)
                    node.relations.add(related_node.index * 4 + NEXT_1_1_OFFSET)

                elif node.nextAssignment == has_assignment and node.nextNextAssignment == 0:
                    node.relations.add(related_node.index * 4 + NEXT_0_0_OFFSET)
                    node.relations.add(related_node.index * 4 + NEXT_0_1_OFFSET)

        # Iteratively remove unnecessary nodes and relations
        unnecessary_nodes = True
        while unnecessary_nodes:
            unnecessary_nodes = False
            for i in range(len(predictive_nodes)):
                node = predictive_nodes[i]
                if len(node.relations) == 0:
                    deleted_index = node.index
                    del predictive_nodes[i]
                    unnecessary_nodes = True
                    # remove all relations to the deleted index
                    for j in range(len(predictive_nodes)):
                        if deleted_index in predictive_nodes[j].relations:
                            predictive_nodes[j].relations.remove(deleted_index)
                    break
        predictive_nodes = SystemUtils.fix_predictive_indexing(predictive_nodes)
        return KripkeStructure(predictive_nodes)

    @staticmethod
    def fix_predictive_indexing(nodes_lst):
        original_nodes = nodes_lst
        for i in range(len(original_nodes)):
            if original_nodes[i].index != i:
                # fix index:
                prev_index = original_nodes[i].index
                original_nodes[i].index = i
                # fix pointing relations
                for j in range(len(original_nodes)):
                    if prev_index in original_nodes[j].relations:
                        original_nodes[j].relations.discard(prev_index)
                        original_nodes[j].relations.add(i)
        return original_nodes
