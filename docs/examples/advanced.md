# Advanced examples

The basic examples show the minimal workflow. These pages work with larger
datasets and dig into the structure the trees produce. Each example is also a
runnable script in the [`examples/`](https://github.com/SealtielFreak/ktree/tree/main/examples)
directory.

## KDTree over many random 5-D points

A k-d tree splits one axis at a time and cycles through dimensions. With enough
points you can observe clusters appearing at increasing `level` (recursion
depth):

```python
import random

from ktree.kdtree import KDTree

N_DIMENSION = 5
N_POINTS = 20

random.seed(42)

tree = KDTree([(-5.0, 5.0) for _ in range(N_DIMENSION)])

points = [
    [random.uniform(-5.0, 5.0) for _ in range(N_DIMENSION)]
    for _ in range(N_POINTS)
]

for p in points:
    tree.insert(p)

clusters = tree.sort()
clusters.sort(key=lambda c: c.level)

print(f"Inserted {N_POINTS} points in {N_DIMENSION}D.")
print(f"sort() produced {len(clusters)} clusters.")

for cluster in clusters:
    print(f"level={cluster.level} shape={cluster.shape} n={len(cluster)}")
```

Run it with:

```bash
uv run python examples/advanced_kdtree.py
```

## Deep Octree with duplicates

`NTreeStatic` bisects every axis at each level, so `limit_divisions` controls
how many times the space is subdivided. Duplicate points are kept in the same
leaf cluster:

```python
from ktree import NTreeStatic

tree = NTreeStatic(
    [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)],
    limit_divisions=5,
)

tree.insert([0.1, 0.1, 0.1])
tree.insert([0.1, 0.025, 0.1])
tree.insert([0.1, 0.025, 0.1])  # duplicate
tree.insert([0.01, 0.2, 0.2])
tree.insert([0.01, 0.5, 0.1])

for cluster in tree.sort():
    print(cluster.shape)
    print(cluster.data)
```

## NTreeDynamic clustering with centroids

`NTreeDynamic` computes its bounding box from the inserted data, which makes it
a convenient clustering primitive. Here we sample a Gaussian mixture and print
the centroid of every returned cluster (based on `examples/d_ntree.py`):

```python
import numpy as np

from ktree.ntree import NTreeDynamic


def generate_dataset(centers, stds, n_samples=500, ndim=3):
    X = []
    y = []

    for i, center in enumerate(centers):
        cluster = np.random.normal(
            loc=center, scale=stds[i], size=(n_samples // len(centers), ndim)
        )
        X.append(cluster)
        y.append(np.full(n_samples // len(centers), i))

    return np.vstack(X), np.concatenate(y)


tree = NTreeDynamic(1, limit_size=10)

data, _ = generate_dataset(
    [[1, 1, 1], [3, 3, 3], [2, 2, 1]], stds=[0.5, 0.5, 0.5], n_samples=500
)

for a in data:
    tree.insert(a)

clusters = sorted(tree.sort(), key=lambda x: len(x), reverse=True)

for node in clusters:
    c_data = np.array(node.data)
    print("Shape:", node.shape)
    print("Centroid:", np.mean(c_data, axis=0))
```

Run it with:

```bash
uv run python examples/d_ntree.py
```

## Static vs. dynamic bounding box

The static tree takes a caller-provided bounding box; the dynamic tree derives
its box from the minimum and maximum coordinates of the inserted points. On the
same data, both partition identically, but the dynamic box is tighter:

```python
from ktree.ntree import NTreeDynamic, NTreeStatic

points = [
    [0.1, 0.1],
    [0.9, 0.9],
    [0.4, 0.6],
    [0.7, 0.2],
    [0.2, 0.8],
    [0.5, 0.5],
]

static = NTreeStatic([(0.0, 1.0), (0.0, 1.0)], limit_divisions=2)
dynamic = NTreeDynamic(limit_divisions=2)

for p in points:
    static.insert(p)
    dynamic.insert(p)

print("Static bounding box (fixed by caller):", static.shape)

dynamic.sort()
print("Dynamic bounding box (computed from data):", dynamic.shape)

print("Static clusters:", len(static.sort()))
print("Dynamic clusters:", len(dynamic.sort()))
```

Run it with:

```bash
uv run python examples/compare_static_dynamic.py
```
