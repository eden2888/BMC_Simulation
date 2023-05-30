import random

import jsonpickle
import networkx as nx
from matplotlib import figure, pyplot as plt
from z3 import *
from KripkeStructureFramework.KripkeStructure import KripkeStructure
from KripkeStructureFramework.Node import Node
from Utils import VisualUtils
from Utils.SystemUtils import SystemUtils
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Utils.SystemFactory import SystemFactory
from Utils.T_Matrix import T_Matrix
from Tests import TestsMethods


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


def test_predictive():
    # m1 :
    s0 = Node(0, isInitial=True)
    s1 = Node(1, assignment='p')
    s2 = Node(2, assignment='p')
    s0.add_relation(0)
    s0.add_relation(1)
    s0.add_relation(2)
    s1.add_relation(0)
    s1.add_relation(1)
    s1.add_relation(2)
    s2.add_relation(0)
    s2.add_relation(1)
    s2.add_relation(2)
    m1 = KripkeStructure([s0, s1, s2])
    return m1


if __name__ == '__main__':
    # ks1, ks2 = create_test_structures()
    # predictive_ks1 = SystemUtils.create_predictive_kripke_structure(ks1)
    # predictive_ks2 = SystemUtils.create_predictive_kripke_structure(ks2)
    # SystemUtils.save_system(predictive_ks1, path='C://BMC_Systems//s1_predictive.json')
    # SystemUtils.save_system(predictive_ks2, path='C://BMC_Systems//s2_predictive.json')

    # generate small and large systems:
    # TestsMethods.prepare_test_1_systems()

    # load systems from files:
    s2, s1 = TestsMethods.load_systems_for_test_1()
    results_large_simulators = TestsMethods.simulate_s1_list_with_s2_list(s1, s2, prediction_variables=False)
    results_small_simulators = TestsMethods.simulate_s1_list_with_s2_list(s2, s1, prediction_variables=False)
    print(results_large_simulators)
    print(results_small_simulators)
