# KTree

![Python - Version](https://img.shields.io/badge/python-%3E%3D3.10-brightgreen)
![PyPI - Version](https://img.shields.io/pypi/v/ktree?color=green&label=pip%20install%20ktree)
![Python - Implementation](https://img.shields.io/pypi/implementation/ktree)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/ktree)
![Docs](https://img.shields.io/badge/docs-mkdocs-blue)
![License](https://img.shields.io/badge/license-0BSD-green)

## Description

KTree is a lightweight library of hierarchical spatial partitioning
structures written in pure Python. The core idea behind all three containers is
the same: recursively subdivide an N-dimensional axis-aligned bounding box into
smaller nested regions, so that spatially close points end up in the same
cluster. This hierarchical decomposition is the foundation of many spatial
data-structure algorithms, including nearest-neighbor search, range queries,
and collision detection, and it is the pattern first formalized for
multidimensional data by Bentley [@bentley-1975].

All containers share a common interface — create the tree, `insert()` points,
then call `sort()` to partition them into clusters. Each cluster exposes its
geometric `shape` (the bounding box it covers) and its `data` (the points that
fell into it). The package is intentionally small and has only one runtime
dependency: NumPy.

### KDTree

`KDTree` is a K-dimensional tree that performs a binary, axis-aligned
partitioning of the search space. At each recursion level the current bounding
box is split along a single axis at the midpoint of that axis' interval, and
the splitting dimension cycles through the axes in round-robin fashion
(dimension `depth mod K`). Every visited region is emitted as a
`KDCluster`, so the output of `sort()` is a sequence of clusters ordered by the
recursion depth at which they were created.

The k-d tree was introduced by Bentley for associative searching in
multidimensional key spaces [@bentley-1975], and its neighborhood-computation
properties are analyzed in detail by Skrodzki [@skrodzki-2019].

### NTreeStatic (NTree)

`NTreeStatic` is the N-dimensional generalization of the classic quadtree and
octree. Instead of splitting a single axis per level, every axis of the current
bounding box is bisected simultaneously at each subdivision step, producing
`2^N` child regions per parent:

- **2D** — each region is split into 4 quadrants: a **QuadTree**,
  first described by Finkel and Bentley [@finkel-1974].
- **3D** — each region is split into 8 octants: an **Octree**,
  as used in volumetric and graphics applications
  [@globus-1991; @madeira-2011].
- **N-D** — the same rule produces `2^N` sub-regions, so the structure works
  for arbitrary dimensionality, not just 2 or 3.

`limit_divisions` controls the maximum recursion depth (how many times the
bounding box may be subdivided). The root bounding box is fixed at construction
time and every inserted point must fall inside it.

### NTreeDynamic

`NTreeDynamic` is the same N-ary partitioning structure as `NTreeStatic` — in
2D it behaves like a QuadTree, in 3D like an Octree, and in general N-D it
bisects every axis to form `2^N` child regions — but the root bounding box is
not provided by the caller. Instead, it is computed during `sort()` from the
minimum and maximum coordinate values of the inserted points on every axis.
This makes the tree self-configuring: it can be used when the search space is
unknown in advance, and it adapts to whatever data is inserted.

## Quickstart

```python
from ktree import NTreeStatic

# A 2D QuadTree over the unit square, with 2 subdivisions.
tree = NTreeStatic([(0.0, 1.0), (0.0, 1.0)], limit_divisions=2)

tree.insert([0.1, 0.1])
tree.insert([0.01, 0.2])
tree.insert([0.01, 0.5])

for cluster in tree.sort():
    print(cluster)
    print(cluster.data)
```

## Install

### From pip

```bash
pip install ktree
```

### From GitHub

```bash
pip install git+https://github.com/SealtielFreak/ktree.git
```

## What next?

- Read the [Usage guide](usage.md) for a walkthrough of every tree type.
- Work through the [basic examples](examples/basic.md) and the
  [advanced examples](examples/advanced.md) for runnable demos.
- Browse the [API reference](api/tree.md) for module, class, and function
  documentation.

## Development

This project uses [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run ruff check src examples
uv run mypy src/
uv run mkdocs serve
```

## License

KTree is released under the
[BSD Zero Clause (0BSD) license](https://github.com/SealtielFreak/ktree/blob/main/LICENSE.md).
