import jsonpickle
from z3 import *
from KripkeStructureFramework.KripkeStructure import KripkeStructure
from KripkeStructureFramework.Node import Node
from Utils.SystemUtils import SystemUtils
from Utils.SystemFactory import SystemFactory
from Utils.T_Matrix import T_Matrix
import PySide6.QtCore


def z3_tests():
    x = Bool("x")
    y = Bool("y")
    x_or_y = Or([x, y])  # disjunction
    x_and_y = And([x, y])  # conjunction
    not_x = Not(x)  # negation
    print(type(x_and_y))
    x_or_y_iff_not_x = x_and_y == not_x
    s = Solver()  # create a solver s

    s.add(x_and_y)  # add the clause: x or y
    s.add(not_x)
    #  z = Bool("z")
    # s.add(Not(z))
    # print(s.check())
    # print(s.model())
    # demo 2:
    s2 = Solver()
    node_indexes = BoolVector('i', 5)
    s2.add(And([node_indexes[0], node_indexes[1], node_indexes[2]]))  # i1 AND i2 AND i3
    s2.add(Not(node_indexes[0]))  # + Not i1
    temp_str = s2.__str__()
    print(temp_str)

    s3 = Solver()
    print(eval(temp_str))


def create_test_structures():
    # m1 :
    s0 = Node(0, isInitial=True)
    s1 = Node(1)
    s2 = Node(2)
    s3 = Node(3, assignment='p')
    s4 = Node(4)
    s0.add_relation(1)
    s0.add_relation(2)
    s1.add_relation(3)
    s2.add_relation(4)
    s3.add_relation(3)
    s4.add_relation(4)
    m1 = KripkeStructure([s0, s1, s2, s3, s4])
    # m2:
    t0 = Node(0, isInitial=True)
    t1 = Node(1)
    t2 = Node(2, assignment='p')
    t3 = Node(3)
    t0.add_relation(1)
    t1.add_relation(2)
    t1.add_relation(3)
    t2.add_relation(2)
    t3.add_relation(3)
    m2 = KripkeStructure([t0, t1, t2, t3])
    return m1, m2


if __name__ == '__main__':
    # Prints PySide6 version
    print(PySide6.__version__)

    # Prints the Qt version used to compile PySide6
    print(PySide6.QtCore.__version__)
    

    # ks1 = SystemFactory.create_system(size=3, initials_density=0, density=100)
    # ks2 = SystemFactory.create_system(size=2, initials_density=0, density=100, attribute_probability=30)
    ks1, ks2 = create_test_structures()
    T = T_Matrix(ks1.get_size(), ks2.get_size())
    i_1 = SystemUtils.get_i_formula(ks1, 'x')
    i_2 = SystemUtils.get_i_formula(ks2, 'y')
    c = i_1.children()
    # print assignments:
    for node in ks1.get_nodes():
        print("ks1 index: " + str(node.index) + " ks1 assignment: " + str(node.assignment) + " initial: " + str(
            node.isInitial))
    for node in ks2.get_nodes():
        print("ks2 index: " + str(node.index) + " ks2 assignment: " + str(node.assignment) + " initial: " + str(
            node.isInitial))
    # create T[m,n]:
    alpha1 = SystemUtils.create_alpha_1(ks1, ks2, T)
    print('Alpha 1: \n' + str(alpha1))
    alpha2 = SystemUtils.create_alpha_2(ks1, ks2, T)
    print('Alpha 2: \n' + str(alpha2))
    alpha3 = SystemUtils.create_alpha_3(ks1, ks2, T)
    print('Alpha 3: \n' + str(alpha3))
    s = Solver()
    s.add(alpha1)
    s.add(alpha2)
    s.add(alpha3)
    print(s.check())
    if s.check() != unsat:
        print(s.model())


    def pickle_test():
        frozen = jsonpickle.encode(ks)
        thawed = jsonpickle.decode(frozen)
        print(type(thawed))
        newKS = KripkeStructure(thawed)
        return newKS
