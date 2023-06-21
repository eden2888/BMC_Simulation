import random
import datetime
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


def test_1_main():
    # original kripke structure - for reference
    m1, m2 = create_test_structures()

    currentDT = datetime.datetime.now()
    print('Started Running - ' + str(currentDT))
    # generate small and large systems:
    TestsMethods.prepare_test_1_systems()
    currentDT = datetime.datetime.now()
    print('Systems created - ' + str(currentDT))
    # load systems from files:
    small, large = TestsMethods.load_systems_for_test_1()
    small.append(m1)
    large.append(m2)
    currentDT = datetime.datetime.now()
    print('Systems Loaded - ' + str(currentDT))
    results_small_simulators = TestsMethods.simulate_s1_list_with_s2_list(small, large, prediction_variables=True)
    currentDT = datetime.datetime.now()
    print('Finished simulating small with large ' + str(currentDT))
    print('Results:')
    print(results_small_simulators)
    results_large_simulators = TestsMethods.simulate_s1_list_with_s2_list(large, small, prediction_variables=True)
    currentDT = datetime.datetime.now()
    print('Finished simulating large with small ' + str(currentDT))
    print('Results:')
    print(results_large_simulators)


if __name__ == '__main__':
    # 4 small systems (2-5), 4 medium (5-15), 4 large(15-30)
    baseSimulationSet = TestsMethods.prepare_test_2_systems()
    # prepare sets to simulate with: sizes 5,15,30,45,60, 70?

    set10SystemsWith5Nodes = TestsMethods.prepare_random_systems(10, [5, 5])
    set10SystemsWith15Nodes = TestsMethods.prepare_random_systems(10, [15, 15])
    set10SystemsWith30Nodes = TestsMethods.prepare_random_systems(10, [30, 30])
    set10SystemsWith45Nodes = TestsMethods.prepare_random_systems(10, [45, 45])
    set10SystemsWith60Nodes = TestsMethods.prepare_random_systems(10, [60, 60])
    set10SystemsWith70Nodes = TestsMethods.prepare_random_systems(10, [70, 70])

    currentDT = datetime.datetime.now()
    print('Starting test: 10 systems with 5 nodes each, simulating 12 systems set ' + str(currentDT))
    res = TestsMethods.simulate_s1_list_with_s2_list(baseSimulationSet, set10SystemsWith5Nodes,
                                                     prediction_variables=True)
    currentDT = datetime.datetime.now()
    print('results: ')
    print(res)
    print('Systems Simulated- ' + str(currentDT))

    currentDT = datetime.datetime.now()
    print('Starting test: 10 systems with 15 nodes each, simulating 12 systems set ' + str(currentDT))
    res = TestsMethods.simulate_s1_list_with_s2_list(baseSimulationSet, set10SystemsWith15Nodes,
                                                     prediction_variables=True)
    currentDT = datetime.datetime.now()
    print('results: ')
    print(res)
    print('Systems Simulated- ' + str(currentDT))

    currentDT = datetime.datetime.now()
    print('Starting test: 10 systems with 30 nodes each, simulating 12 systems set ' + str(currentDT))
    res = TestsMethods.simulate_s1_list_with_s2_list(baseSimulationSet, set10SystemsWith30Nodes,
                                                     prediction_variables=True)
    currentDT = datetime.datetime.now()
    print('results: ')
    print(res)
    print('Systems Simulated- ' + str(currentDT))

    currentDT = datetime.datetime.now()
    print('Starting test: 10 systems with 45 nodes each, simulating 12 systems set ' + str(currentDT))
    res = TestsMethods.simulate_s1_list_with_s2_list(baseSimulationSet, set10SystemsWith45Nodes,
                                                     prediction_variables=True)
    currentDT = datetime.datetime.now()
    print('results: ')
    print(res)
    print('Systems Simulated- ' + str(currentDT))

    currentDT = datetime.datetime.now()
    print('Starting test: 10 systems with 60 nodes each, simulating 12 systems set ' + str(currentDT))
    res = TestsMethods.simulate_s1_list_with_s2_list(baseSimulationSet, set10SystemsWith60Nodes,
                                                     prediction_variables=True)
    currentDT = datetime.datetime.now()
    print('results: ')
    print(res)
    print('Systems Simulated- ' + str(currentDT))

    currentDT = datetime.datetime.now()
    print('Starting test: 10 systems with 70 nodes each, simulating 12 systems set ' + str(currentDT))
    res = TestsMethods.simulate_s1_list_with_s2_list(baseSimulationSet, set10SystemsWith70Nodes,
                                                     prediction_variables=True)
    currentDT = datetime.datetime.now()
    print('results: ')
    print(res)
    print('Systems Simulated- ' + str(currentDT))

    # currentDT = datetime.datetime.now()
    # print('Systems created - ' + str(currentDT))
    # res = TestsMethods.simulate_s1_list_with_s2_list(m1, m2, prediction_variables=False)
    # currentDT = datetime.datetime.now()
    # print('Systems Simulated without pred vars - ' + str(currentDT))
    # res = TestsMethods.simulate_s1_list_with_s2_list(m1, m2, prediction_variables=True)
    # currentDT = datetime.datetime.now()
    # print('Systems Simulated with pred vars - ' + str(currentDT))

    # original kripke structure - for reference
    # m1, m2 = create_test_structures()
    #
    # currentDT = datetime.datetime.now()
    # print('Started Running - ' + str(currentDT))
    # # generate small and large systems:
    # TestsMethods.prepare_test_2_systems()
    # currentDT = datetime.datetime.now()
    # print('Systems created - ' + str(currentDT))
    # # load systems from files:
    # set1, set2 = TestsMethods.load_systems_for_test_2()
    # set1.append(m1)
    # set2.append(m2)
    # currentDT = datetime.datetime.now()
    # print('Systems Loaded - ' + str(currentDT))
    # results_small_simulators = TestsMethods.simulate_s1_list_with_s2_list(set1, set2, prediction_variables=True)
    # currentDT = datetime.datetime.now()
    # print('Finished simulating set1 with set2 ' + str(currentDT))
    # print('Results:')
    # print(results_small_simulators)
    # results_large_simulators = TestsMethods.simulate_s1_list_with_s2_list(set1, set2, prediction_variables=True)
    # currentDT = datetime.datetime.now()
    # print('Finished simulating set1 with set2 ' + str(currentDT))
    # print('Results:')
    # print(results_large_simulators)
