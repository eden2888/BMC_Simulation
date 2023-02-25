from KripkeStructureFramework.Node import Node
import random

from KripkeStructureFramework.Relation import Relation


class SystemFactory:

    @staticmethod
    def create_system(density=10, size=10, attribute="q", initials_density=10, attribute_probability=30):
        """
        :param density: Structure's density: between 0 to 100 percents.
        :type density: int, float
        :param size: number of nodes in the structure
        :type size: int
        :param attribute: attributes that may be added to each node
        :type attribute: list of strings
        :param initials_density: represents the amount of initial states, 10 means 10% of nodes are initials, 0 means 1 initial node
        :type initials_density: int
        :param attribute_probability: the probability of an attribute to appear on a node, between 0 to 100.
        :type attribute_probability: int
        :return: Kripke structure with the desired parameters
        :rtype:  KripkeStructure
        """
        nodes = []
        relations = []
        num_of_initials = size * (initials_density/100)
        if num_of_initials < 1:
            num_of_initials = 1
        if num_of_initials > size:
            num_of_initials = size
        # create nodes:
        for i in range(0, size):
            attributes = [attribute, ""]
            # node_attribute will store a list of 1 attribute according to the given probability:
            node_attribute = random.choices(attributes, weights=[attribute_probability, 100-attribute_probability], k=1)
            # create a new node according the our parameters:
            nodes.append(Node(i, node_attribute[0], num_of_initials > 0))
            num_of_initials = num_of_initials - 1
        # create relations:
        # minimum relations amount at 0%: size
        # maximum relations amount at 100%: size^2
        # generate minimum required relations:
        node_ids = list(range(0, size))
        random.shuffle(node_ids)
        # get random initial node:
        for node_id in node_ids:
            if nodes[node_id].isInitial:
                first_node = node_id
                node_ids.pop(node_ids.index(first_node))
                break
        #create the minimum relations"
        current_node_id = first_node
        for i in node_ids:
            # relations.append(Relation(nodes[current_node_id], nodes[i]))
            relations.append(Relation(current_node_id, i))
            current_node_id = i
        # now connect last node to another node:
        rand_node_id = random.randint(0, size)
        # relations.append(Relation(nodes[current_node_id], nodes[rand_node_id]))
        relations.append(Relation(current_node_id, rand_node_id))
        return nodes, relations
