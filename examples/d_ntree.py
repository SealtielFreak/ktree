import random

import numpy as np

from ktree.ntree import NTreeDynamic

N_DIMENSION = 3

random.seed(0)

tree = NTreeDynamic(1)

for a in range(30):
    data = np.random.uniform(-1, 1, 3)
    tree.insert(data)

sorted_data = tree.sort()
sorted_data = sorted(sorted_data, key=lambda x: len(x))[::-1]

for n, node in enumerate(sorted_data):
    print("Shape: ", node.shape)

    c_data = np.array(node.data)
    centroid = np.mean(c_data, axis=0)

    print("Centroid:", centroid)
