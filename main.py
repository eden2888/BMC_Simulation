import jsonpickle
from z3 import *
from KripkeStructureFramework.KripkeStructure import KripkeStructure
from KripkeStructureFramework.KripkeStructure import Node
from Utils.SystemUtils import SystemUtils
from Utils.SystemFactory import SystemFactory
from Utils.T_Matrix import T_Matrix


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


if __name__ == '__main__':
    ks1 = SystemFactory.create_system(size=2, initials_density=100, density=100)
    ks2 = SystemFactory.create_system(size=2, initials_density=100, density=100)
    T = T_Matrix(ks1.get_size(), ks2.get_size())
    i_1 = SystemUtils.get_i_formula(ks1, 'x')
    i_2 = SystemUtils.get_i_formula(ks2, 'y')
    c = i_1.children()
    #print assignments:
    for node in ks1.get_nodes():
        print("ks1 index: " + str(node.index) + " ks1 assignment: " + str(node.assignment))
    for node in ks2.get_nodes():
        print("ks2 index: " + str(node.index) + " ks2 assignment: " + str(node.assignment))
    # create T[m,n]:
    alpha1 = SystemUtils.create_alpha_1(ks1, ks2, T)
    print(alpha1)
    alpha2 = SystemUtils.create_alpha_2(ks1, ks2, T)
    print(alpha2)
    s = Solver()
    s.add(alpha1)
    s.add(alpha2)
    print(s.check())
    print(s.model())
            #if is_expr(alpha1):
             #   alpha1 = Or(alpha1, T[q.index][t.index])




    # for state in i_1.children():
    #     if is_expr(final_exp):
    #         final_exp = And([final_exp, And([state, i_2])])
    #     else:
    #         final_exp = And([state, i_2])
   # print(final_exp)
   # print(simplify(final_exp))
    #output = ks.get_initials()

    def pickle_test():
        frozen = jsonpickle.encode(ks)
        thawed = jsonpickle.decode(frozen)
        print(type(thawed))
        newKS = KripkeStructure(thawed)
        return newKS
