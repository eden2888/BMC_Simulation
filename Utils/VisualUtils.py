# import the modules
import os
import networkx as nx
import matplotlib.pyplot as plt
from KripkeStructureFramework.KripkeStructure import KripkeStructure
from KripkeStructureFramework.Node import Node
from Utils.SystemFactory import SystemFactory
from Utils.SystemUtils import SystemUtils
import graphviz


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


@staticmethod
def preview_system(system):
    colors_lst = SystemUtils.get_node_color_list(system)
    sys1_relations = SystemUtils.get_relations_list(system)
    node_names = SystemUtils.get_node_names_dictionary(system)
    # Create the graph
    G = nx.MultiDiGraph()
    G.add_edges_from(sys1_relations)
    # Visualize
    nx.draw(G, with_labels=True, labels=node_names, node_size=800, node_color=colors_lst, pos=nx.kamada_kawai_layout(G))
    #return plt#.show()

@staticmethod
def preview_system_test():
    s1, s2 = create_test_structures()
    system = s1
    colors_lst = SystemUtils.get_node_color_list(system)
    sys1_relations = SystemUtils.get_relations_list(system)
    node_names = SystemUtils.get_node_names_dictionary(system)
    # Create the graph
    G = nx.MultiDiGraph()
    G.add_edges_from(sys1_relations)
    # Visualize
    nx.draw(G, with_labels=True, labels=node_names, node_size=800, node_color=colors_lst, pos=nx.kamada_kawai_layout(G))
    return G, node_names, colors_lst, plt
@staticmethod
def preview_system(system):
    colors_lst = SystemUtils.get_node_color_list(system)
    sys1_relations = SystemUtils.get_relations_list(system)
    node_names = SystemUtils.get_node_names_dictionary(system)
    # Create the graph
    G = nx.MultiDiGraph()
    G.add_edges_from(sys1_relations)
    # Visualize
    nx.draw(G, with_labels=True, labels=node_names, node_size=800, node_color=colors_lst, pos=nx.kamada_kawai_layout(G))
    return G, node_names, colors_lst, plt

@staticmethod
def store_test_systems():
    s1, s2 = create_test_structures()
    SystemUtils.save_system(s1, 'D:\Test\s1.json')
    SystemUtils.save_system(s2, 'D:\Test\s2.json')

#s1,s2 = create_test_structures()
#temp = preview_system(s1)
#temp.show()