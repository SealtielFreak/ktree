import random

import numpy as np

from ktree.ntree import NTreeMean

N_DIMENSION = 3

def generate_dataset(centers, stds, n_samples=500, ndim=3):
    X = []
    y = []

    for i, center in enumerate(centers):
        cluster = np.random.normal(loc=center, scale=stds[i], size=(n_samples // len(centers), ndim))
        X.append(cluster)
        y.append(np.full(n_samples // len(centers), i))

    return np.vstack(X), np.concatenate(y)


tree = NTreeMean(3)

data, ground_truth = generate_dataset(
    [[1, 1, 1], [3, 3, 3], [2, 2, 1]],
    stds=[.5, .5, .5],
    n_samples=5000 * 5000
)

for a in data:
    tree.insert(a)

sorted_data = tree.sort()
sorted_data = sorted(sorted_data, key=lambda x: len(x))[::-1]

for n, node in enumerate(sorted_data):
    print("Shape: ", node.shape)

    c_data = np.array(node.data)
    centroid = np.mean(c_data, axis=0)

    print("Centroid:", centroid)
