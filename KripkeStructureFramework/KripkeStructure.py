from KripkeStructureFramework import Node


class KripkeStructure:
    def __init__(self, nodes):
        if not (isinstance(nodes, list)):
            raise ValueError(f"Invalid input for nodes !")
        self.__nodes = nodes

    def get_initials(self):
        # return filter(lambda node: node.isInitial == True , self.__nodes)
        return [node for node in self.__nodes if node.is_initial]

    def get_nodes(self):
        return self.__nodes

    def get_size(self):
        return len(self.__nodes)