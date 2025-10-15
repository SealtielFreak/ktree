import random

from ktree.kdtree import KDTree

N_DIMENSION = 5

random.seed(0)

tree = KDTree([(-5, 5) for _ in range(N_DIMENSION)])

for _ in range(5):
    tree.insert([random.uniform(-5, 5) for _ in range(N_DIMENSION)])

for cluster in tree.sort():
    print(cluster)
    print(cluster.data)
