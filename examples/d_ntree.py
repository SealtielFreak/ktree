import random

import numpy as np

from ktree.ntree import NTreeDynamic

N_DIMENSION = 3

random.seed(0)

tree = NTreeDynamic(2)
data = np.random.uniform(0, 64, (32 * 32, 3))

for a in data:
    tree.insert(a)

sorted_data = tree.sort()

for n, (shape, data) in enumerate(sorted_data):
    print(f"Shape[{n}]:", shape)
    # print(len(data), data)

print(tree.shape)
