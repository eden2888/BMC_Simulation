import random

import jsonpickle

from KripkeStructureFramework.KripkeStructure import KripkeStructure
from SystemFactory import SystemFactory

if __name__ == '__main__':
    ks = SystemFactory.create_system(density=100)
    #frozen = jsonpickle.encode(ks)
    #thawed = jsonpickle.decode(frozen)
    #print(type(thawed))
    #newKS = KripkeStructure(thawed)
    SystemFactory.export_system("", "test_json.json", ks)
    ks2 = SystemFactory.import_system("test_json.json")
    print("done")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
