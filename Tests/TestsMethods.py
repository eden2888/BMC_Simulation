import random

from z3 import *
from Utils.SystemUtils import SystemUtils
from Utils.SystemFactory import SystemFactory


def prepare_random_systems(amount, sizeRange):
    '''
    creates 'amount' list of random systems according to the range size.
    :param sizeRange: range of systems sizes
    :type sizeRange: [min_size,max_size], e.g: [1,15]
    :param amount: amount of systems to create
    :type amount: Integer
    :return: list of systems
    :rtype: List
    '''
    systems = []
    for i in range(0, amount):
        # randomize values:
        density = random.randint(10, 15)
        size = random.randint(sizeRange[0], sizeRange[1])
        systems.append(SystemFactory.create_system(density=density, size=size))
    return systems


def saveListOfSystems(systems, name_prefix, path = 'C://BMC_Systems//'):
    """
    For a given list of systems and a prefix, saves the systems as json files
    :param path: folder to store the files in
    :type path:  str
    :param systems: list of Kripke structures
    :type systems: list of KripkeStructures
    :param name_prefix: file name prefix
    :type name_prefix: str
    :return: none
    :rtype:
    """
    i = 1
    for s in systems:
        SystemUtils.save_system(s, path=path + name_prefix + '-' + str(i) + '.json')
        i += 1


def prepare_test_1_systems():
    """
    Test 1: test the behaviour of simulation between small and large density systems.
    :return:
    :rtype:
    """
    small_systems = prepare_random_systems(20, [2, 5])
    large_systems = prepare_random_systems(20, [10, 30])
    # store systems on file system for tests consistency:
    saveListOfSystems(small_systems, 'small(2-5)')
    saveListOfSystems(large_systems, 'large(10-30)')

def prepare_test_2_systems():
    """
    Test 2: test the behaviour of simulation between two sets of systems with the same size.
    :return:
    :rtype:
    """
    set1 = prepare_random_systems(4, [2, 5])
    set2 = prepare_random_systems(4, [5, 15])
    set3 = prepare_random_systems(4, [15, 30])
    # store systems on file system for tests consistency:
    return set1+set2+set3


def load_systems_list(path, prefix):
    """
    returns a list of systems that exists in the given path and have the given prefix
    :param path: files path
    :type path: str
    :param prefix: files prefix name
    :type prefix:  str
    :return: list of KripkeStructures
    :rtype: list of KripkeStructures
    """
    systems = []
    files = [filename for filename in os.listdir(path) if filename.startswith(prefix)]
    for file in files:
        systems.append(SystemUtils.load_system(path + file))
    return systems


def load_systems_for_test_1():
    """
    Loads the default files for test #1
    :return: 2 lists of systems, 1 small and 1 large.
    :rtype:tuple
    """
    small_systems = load_systems_list('C://BMC_Systems//', 'small(2-5)')
    large_systems = load_systems_list('C://BMC_Systems//', 'large(10-30)')
    return small_systems, large_systems


def load_systems_for_test_2():
    """
    Loads the default files for test #1
    :return: 2 lists of systems of the same size
    :rtype:tuple
    """
    set1 = load_systems_list('C://BMC_Systems//', 'set1')
    set2 = load_systems_list('C://BMC_Systems//', 'set2')
    return set1, set2


def simulate_s1_list_with_s2_list(s1, s2, prediction_variables=True):
    """
    For a given systems lists s1,s2, attempts to simulate every sys in s1 with every sys in s2
    :param prediction_variables: If true, use prediction variables algorithm
    :type prediction_variables: bool
    :param s1: list of systems
    :type s1: list
    :param s2: list of systems
    :type s2: list
    :return: results of each system and the simulations success/fail
    :rtype: dict
    """
    results = {}
    for first in s1:
        for second in s2:
            if prediction_variables:
                predictive_first_sys = SystemUtils.create_predictive_kripke_structure(first)
                checker = SystemUtils.check_simulation(predictive_first_sys, second)
            else:
                checker = SystemUtils.check_simulation(first, second)

            # store data in dictionary
            if first not in results:
                results[first] = []
            results[first].append(checker.check())
    # results now store a dictionary of (system:[list of True/False according to simulation success]
    return results
