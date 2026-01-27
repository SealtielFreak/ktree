import random

from ktree.ntree import NTreeStatic

N_DIMENSION = 3

random.seed(0)

tree = NTreeStatic([(0., 1.) for _ in range(N_DIMENSION)], 1)

for _ in range(3):
    tree.insert([random.uniform(0, 1) for _ in range(N_DIMENSION)])

for nodes in tree.sort():
    print(nodes)
    print(nodes.data)
