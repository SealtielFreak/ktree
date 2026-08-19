# KTree

![Python - Version](https://img.shields.io/badge/python-%3E%3D3.10-brightgreen)
![PyPI - Version](https://img.shields.io/pypi/v/ktree?color=green&label=pip%20install%20ktree)
![Python - Implementation](https://img.shields.io/pypi/implementation/ktree)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/ktree)
![Docs](https://img.shields.io/badge/docs-mkdocs-blue)
![License](https://img.shields.io/badge/license-0BSD-green)

KTree provides lightweight, N-dimensional spatial grouping structures in pure Python:

- **KDTree** — recursive axis-aligned splitting over K dimensions.
- **NTree** — configurable N-ary tree that can be used as a
  [QuadTree](https://en.wikipedia.org/wiki/Quadtree) (2D) or
  [Octree](https://en.wikipedia.org/wiki/Octree) (3D).
- **NTreeDynamic** — same idea, but the bounding shape is discovered from the
  inserted data instead of being fixed up front.

The package is intentionally small and has only one runtime dependency: NumPy.

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

The docs cover each tree type, the public API, and runnable examples for
QuadTree, Octree, KDTree, and dynamic NTree use cases.

## Development

This project uses [uv](https://docs.astral.sh/uv/).

```bash
# Install the project and all dev/docs dependencies
uv sync

# Lint and format
uv run ruff check src examples
uv run ruff format src examples

# Type-check
uv run mypy src/

# Run the bundled examples
for f in examples/*.py; do uv run python "$f"; done

# Build the package
uv build

# Build the documentation site
uv run mkdocs build --strict
```

## License

KTree is released under the [BSD Zero Clause (0BSD) license](LICENSE).
