from KripkeStructureFramework import Relation
from KripkeStructureFramework import Node


class KripkeStructure:
    def __init__(self, nodes, relations):
        if not (isinstance(nodes, list)):
            raise ValueError(f"Invalid input for nodes !")
        if not (isinstance(relations, list)):
            raise ValueError(f"Invalid input for relations !")
        self.__nodes = nodes
        self.__relations = relations

    def get_initials(self):
        # return filter(lambda node: node.isInitial == True , self.__nodes)
        return [node for node in self.__nodes if node.is_initial]

    def get_relations(self):
        return self.__relations

    def get_nodes(self):
        return self.__nodes
