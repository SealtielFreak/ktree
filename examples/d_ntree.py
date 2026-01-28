import random

from ktree.ntree import NTreeDynamic

N_DIMENSION = 3

random.seed(0)

tree = NTreeDynamic(1)

for _ in range(30):
    tree.insert([random.randint(0, 64) for _ in range(N_DIMENSION)])

for shape, data in tree.sort():
    print("Shape:", shape)
    print(data)
