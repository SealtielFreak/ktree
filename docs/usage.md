# Usage

KTree ships three tree containers. Pick the one that matches how much you know
about your search space up front.

## Choosing a tree

| Tree | When to use it |
|------|----------------|
| `KDTree` | You want a classic K-dimensional tree with cyclic axis splitting. |
| `NTreeStatic` | You already know the bounding box of your space. Use 2D for a QuadTree or 3D for an Octree. |
| `NTreeDynamic` | You only know the points, not the bounds; the tree computes the bounding box for you. |

## KDTree

`KDTree` performs a binary, axis-aligned partition of the search space. At
each recursion level the current bounding box is split along a single axis at
its midpoint, cycling through dimensions in round-robin order (dimension
`depth mod K`). The k-d tree structure was introduced by Bentley
[@bentley-1975]; see also Skrodzki's analysis of its neighborhood-computation
properties [@skrodzki-2019].

```python
from ktree import KDTree

axis = [(-5, 5), (-5, 5), (-5, 5), (-5, 5), (-5, 5)]
tree = KDTree(axis)

tree.insert([3.4, 2.5, -0.8, -2.4, 0.1])
tree.insert([-0.9, 2.8, -1.9, -0.2, 0.8])
tree.insert([4.0, 0.0, -2.1, 2.5, 1.1])

for cluster in tree.sort():
    print(cluster)
    print(cluster.data)
```

## QuadTree with `NTreeStatic`

A two-dimensional `NTreeStatic` with a fixed unit-square bounding box is a
QuadTree [@finkel-1974]: every subdivision bisects both axes, splitting each
region into 4 quadrants.

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

## Octree with `NTreeStatic`

Add a third dimension and you have an Octree [@globus-1991; @madeira-2011]:
each region is split into 8 octants.

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

## Dynamic NTree

Use `NTreeDynamic` when you do not know the bounding box ahead of time. The
tree computes the bounding box from the inserted data during the first call to
`sort()` — the same N-ary partitioning as `NTreeStatic`, but self-configuring:
QuadTree-like in 2D, Octree-like in 3D, and general `2^N` subdivision in N-D.

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

## Common interface

Every tree follows the same pattern:

1. **Create** the tree with a bounding box (or `limit_divisions` for dynamic
   trees).
2. **Insert** points one at a time with `insert()`.
3. **Partition** with `sort()` to get back clusters.
4. **Iterate** over clusters; each cluster exposes `shape` (its bounds) and
   `data` (the points inside).

The abstract interfaces are documented in [`ktree.tree`](api/tree.md).
