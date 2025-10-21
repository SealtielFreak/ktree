import random

from ktree.kdtree import KDTree


def create_blobs(n, axis):
    a, b = axis

    return [random.uniform(a, b) for _ in range(n)]

N_LENGTH = 100
N_DIMENSION = 3

tree = KDTree([(-5, 5) for _ in range(N_DIMENSION)], 200)

random.seed(0)

data = [
           create_blobs(N_DIMENSION, (1, 2)) for _ in range(N_LENGTH)
       ] + [
           create_blobs(N_DIMENSION, (0, 6)) for _ in range(N_LENGTH)
       ] + [
           create_blobs(N_DIMENSION, (4, 5)) for _ in range(N_LENGTH)
       ] + [
           create_blobs(N_DIMENSION, (-5, -3)) for _ in range(N_LENGTH)
       ] + [
           create_blobs(N_DIMENSION, (-3, -2)) for _ in range(N_LENGTH)
       ]

for d in data:
    tree.insert(d)

clusters = tree.sort()

for cluster in clusters:
    print(cluster)
    # print(cluster.data)

print(len(clusters))
