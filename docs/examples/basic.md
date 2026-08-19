# Basic examples

These examples mirror the [README quickstart](../index.md#quickstart) and show
the minimal workflow for every container: **create → insert → sort → iterate**.

## QuadTree (2D `NTreeStatic`)

```python
from ktree import NTreeStatic

tree = NTreeStatic([(0.0, 1.0), (0.0, 1.0)], limit_divisions=2)

tree.insert([0.1, 0.1])
tree.insert([0.01, 0.2])
tree.insert([0.01, 0.5])

for cluster in tree.sort():
    print(cluster)
    print(cluster.data)
```

## Octree (3D `NTreeStatic`)

```python
from ktree import NTreeStatic

tree = NTreeStatic(
    [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)],
    limit_divisions=2,
)

tree.insert([0.1, 0.1, 0.1])
tree.insert([0.1, 0.025, 0.1])
tree.insert([0.01, 0.2, 0.2])
tree.insert([0.01, 0.5, 0.1])

for cluster in tree.sort():
    print(cluster)
    print(cluster.data)
```

## KDTree

```python
from ktree import KDTree

tree = KDTree([(-5.0, 5.0), (-5.0, 5.0)])

tree.insert([1.0, 2.0])
tree.insert([-2.0, -1.0])
tree.insert([4.0, 4.0])

for cluster in tree.sort():
    print(cluster)
    print(cluster.data)
```

## One-dimensional NTree (`utree`)

```python
from ktree import NTreeStatic

tree = NTreeStatic([(0, 10)], limit_divisions=2)

tree.insert([2])
tree.insert([1])
tree.insert([2])
tree.insert([9])

for cluster in tree.sort():
    print(cluster)
    print(cluster.data)
```

## Dynamic NTree

```python
from ktree import NTreeDynamic

tree = NTreeDynamic(limit_divisions=2)

tree.insert([0.1, 0.1, 0.1])
tree.insert([0.5, 0.5, 0.5])
tree.insert([0.9, 0.9, 0.9])

for cluster in tree.sort():
    print(cluster)
    print(cluster.data)
```

See the [advanced examples](advanced.md) for larger datasets and deeper
analysis.
