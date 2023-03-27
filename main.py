import random
import jsonpickle
import z3
from z3 import *
from KripkeStructureFramework.KripkeStructure import KripkeStructure
from SystemUtils import SystemUtils
from SystemFactory import SystemFactory
from Utils.StateRef import StateRef


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

    ks = SystemFactory.create_system(size=4, initials_density=100) # dummy 2 initial system
    formula = SystemUtils.get_i_formula(ks, 'x')

    #output = ks.get_initials()
    print(formula)
    print('simplified: ')
    print(simplify(formula))
    def pickle_test():
        frozen = jsonpickle.encode(ks)
        thawed = jsonpickle.decode(frozen)
        print(type(thawed))
        newKS = KripkeStructure(thawed)
        return newKS
