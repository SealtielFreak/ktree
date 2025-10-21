import random

from ktree.kdtree import KDTree

N_DIMENSION = 5

random.seed(0)

def create_blobs(n, axis):
    a, b = axis

    return [
        random.uniform(a, b) for _ in range(n)
    ]


tree = KDTree([(-5, 5) for _ in range(N_DIMENSION)], 5)

for _ in range(5):
    tree.insert(create_blobs(N_DIMENSION, (1, 2)))

for _ in range(5):
    tree.insert(create_blobs(N_DIMENSION, (3, 3.5)))

for _ in range(5):
    tree.insert(create_blobs(N_DIMENSION, (-1, 0)))

for _ in range(5):
    tree.insert(create_blobs(N_DIMENSION, (0.5, 1.5)))

for cluster in tree.sort():
    print(cluster)
    print(cluster.data)
