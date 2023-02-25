import random

from SystemFactory import SystemFactory

if __name__ == '__main__':
    nodes, relations = SystemFactory.create_system(initials_density=100)
    print(nodes)
    print(relations)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
