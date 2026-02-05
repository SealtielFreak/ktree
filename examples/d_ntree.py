import random

import numpy as np

from ktree.ntree import NTreeDynamic

N_DIMENSION = 3

random.seed(0)

tree = NTreeDynamic(1)

for a in range(30):
    data = np.random.uniform(0, 64, 3)
    tree.insert(data)

sorted_data = tree.sort()

for n, node in enumerate(sorted_data):
    print(node)
    print(node.data)

print(tree.shape)
