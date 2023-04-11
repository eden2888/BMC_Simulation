# import the modules
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


sys1, sys2 = create_test_structures()
sys3 = SystemFactory.create_system(size = 60, density=0)
colors_lst = SystemUtils.get_node_color_list(sys3)
sys1_relations = SystemUtils.get_relations_list(sys3)
node_names = SystemUtils.get_node_names_dictionary(sys3)
# Create the graph
G = nx.MultiDiGraph()
G.add_edges_from(sys1_relations)
# Visualize
nx.draw(G, with_labels=True, labels=node_names, node_size=800, node_color=colors_lst, pos=nx.spiral_layout(G))
plt.show()
# #  pos=nx.kamada_kawai_layout(G)
