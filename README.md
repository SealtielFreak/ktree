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
multidimensional data by Bentley
([1](#references)).

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
multidimensional key spaces ([1](#references)), and its neighborhood-computation
properties are analyzed in detail by Skrodzki
([2](#references)).

### NTreeStatic (NTree)

`NTreeStatic` is the N-dimensional generalization of the classic quadtree and
octree. Instead of splitting a single axis per level, every axis of the current
bounding box is bisected simultaneously at each subdivision step, producing
`2^N` child regions per parent:

- **2D** — each region is split into 4 quadrants: a **QuadTree**,
  first described by Finkel and Bentley ([3](#references)).
- **3D** — each region is split into 8 octants: an **Octree**,
  as used in volumetric and graphics applications
  ([4](#references), [5](#references)).
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

## Documentation

Full documentation is built with [MkDocs](https://www.mkdocs.org/):

```bash
uv sync
uv run mkdocs serve
```

The docs cover each tree type, the public API, runnable examples, and the
references behind the data structures (see [`references.bib`](references.bib)).

## Testing

The test suite is built with [pytest](https://docs.pytest.org/) and covers every
class and helper in the package. Running the tests also executes the `>>>`
examples embedded in the docstrings and prints a coverage report:

```bash
uv run pytest
```

Run a single test file:

```bash
uv run pytest tests/test_ntree.py
```

## Development

This project uses [uv](https://docs.astral.sh/uv/).

```bash
# Install the project and all dev/docs dependencies
uv sync

# Lint and format
uv run ruff check src tests examples
uv run ruff format src tests examples

# Type-check
uv run mypy src/

# Run the tests (unit tests, doctests, and coverage report)
uv run pytest

# Run the bundled examples
for f in examples/*.py; do uv run python "$f"; done

# Build the package
uv build

# Build the documentation site
uv run mkdocs build --strict
```

## License

[KTree](https://github.com/SealtielFreak/ktree) is released under the [BSD Zero Clause (0BSD) license](LICENSE).

## References

1. Jon Louis Bentley. *Multidimensional binary search trees used for
   associative searching*. Communications of the ACM 18(9): 509–517, 1975.
   <https://doi.org/10.1145/361002.361007>
2. Martin Skrodzki. *The k-d tree data structure and a proof for neighborhood
   computation in expected logarithmic time*. 2019.
   <https://arxiv.org/abs/1903.04936v1>
3. Raphael A. Finkel and Jon Louis Bentley. *Quad trees: a data structure for
   retrieval on composite keys*. Acta Informatica 4(1): 1–9, 1974.
   <https://doi.org/10.1007/BF00288933>
4. Al Globus. *OcTree Optimization*. Proceedings of SPIE 1459: 2–10, 1991.
   <https://doi.org/10.1117/12.44376>
5. Daniel Madeira, Anselmo Montenegro, Esteban Clua, and Thomas Lewiner.
   *GPU octrees and optimized search*. VIII Brazilian Symposium on Games and
   Digital Entertainment, 2011.
   <http://www.sbgames.org/papers/sbgames09/computing/short/cts19_09.pdf>
