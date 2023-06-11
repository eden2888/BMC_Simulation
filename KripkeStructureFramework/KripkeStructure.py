class KripkeStructure:
    '''
    A data type that holds a kripke structure as a set of nodes with connectioncs between them
    '''
    def __init__(self, nodes):
        if not (isinstance(nodes, list)):
            raise ValueError(f"Invalid input for nodes !")
        self.__nodes = nodes

    def get_initials(self):
        return [node for node in self.__nodes if node.isInitial]

    def get_nodes(self):
        return self.__nodes


    def get_size(self):
        return len(self.__nodes)