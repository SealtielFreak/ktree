"""KDTree over many random 5-D points."""

import random

from ktree.kdtree import KDTree

N_DIMENSION = 5
N_POINTS = 20

random.seed(42)

tree = KDTree([(-5.0, 5.0) for _ in range(N_DIMENSION)])

points = [
    [random.uniform(-5.0, 5.0) for _ in range(N_DIMENSION)] for _ in range(N_POINTS)
]

for p in points:
    tree.insert(p)

clusters = tree.sort()
clusters.sort(key=lambda c: c.level)

print(f"Inserted {N_POINTS} points in {N_DIMENSION}D.")
print(f"sort() produced {len(clusters)} clusters.")

for cluster in clusters:
    print(f"level={cluster.level} shape={cluster.shape} n={len(cluster)}")
    print(f"  data={list(cluster.data)}")
