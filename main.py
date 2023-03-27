import jsonpickle
from z3 import *
from KripkeStructureFramework.KripkeStructure import KripkeStructure
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


# print(s3)
# print(node_indexes)
# print(s2.check())
#    print(node_indexes[0])


if __name__ == '__main__':
    # ks = SystemFactory.create_system(density=100)
    # SystemFactory.export_system("", "test_json.json", ks)
    # ks2 = SystemFactory.import_system("test_json.json")

    ks1 = SystemFactory.create_system(size=2, initials_density=100, density=100)
    ks2 = SystemFactory.create_system(size=2, initials_density=100, density=100)
    i_1 = SystemUtils.get_i_formula(ks1, 'x')
    i_2 = SystemUtils.get_i_formula(ks2, 'y')
    c = i_1.children()
    # create T[m,n]:
    alpha1 = SystemUtils.create_alpha_1(ks1, ks2)
    print(alpha1)
    s = Solver()
    s.add(alpha1)
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
