# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- IEEE-formatted references in the documentation, rendered from `references.bib`
  via an `ieee.csl` style and pandoc.
- Basic and advanced example pages in the MkDocs documentation.
- New example scripts: `examples/advanced_kdtree.py` and
  `examples/compare_static_dynamic.py`.

### Changed

- README references converted to IEEE citation format.

## [0.2.1] - 2026-08-19

### Added

- Migrated packaging to `pyproject.toml` with the `hatchling` build backend.
- Dynamic versioning: the package version is read from `__VERSION__` in
  `src/ktree/__init__.py`.
- Standard `src/` layout for the package.
- Ruff linting/formatting and Mypy type-checking, configured in `pyproject.toml`.
- MkDocs documentation site with `mkdocs-material`, `mkdocstrings`, and
  BibTeX-based citations.
- Pytest test suite with coverage (`tests/`).
- CI workflows: `.github/workflows/tests.yml` and
  `.github/workflows/docs.yml`.
- Relicensed under the BSD Zero Clause (0BSD) license (replacing WTFPL).

### Changed

- Replaced `setup.py` / `requirements.txt` / `mypy.ini` with a single
  `pyproject.toml`.
- Rewrote the README with a more technical description and references.
- Expanded docstrings across all public modules, classes, and functions.
- Pinned `numpy>=1.24.4,<2.2`.

### Removed

- `setup.py`, `requirements.txt`, `mypy.ini`, `.pypirc`, `main.py`, and the
  empty `ktree/cluster.py` stub.

## [0.0.2] - 2026-02-06

### Added

- `NTreeDynamic`, a data-driven N-ary tree that computes its bounding box from
  the inserted points.
- Python 3.10 support.

### Changed

- Renamed the original `NTree` to `NTreeStatic`.
- Fixed recursive clustering behavior.
- Switched to setuptools-based packaging.

## [0.0.1] - 2025-10-13

### Added

- Initial release with `KDTree` and `NTreeStatic` (QuadTree / Octree).

[Unreleased]: https://github.com/SealtielFreak/ktree/tree/refactoring/documentation
[0.2.1]: https://github.com/SealtielFreak/ktree/tree/refactoring/documentation
[0.0.2]: https://github.com/SealtielFreak/ktree/releases/tag/v0.0.2
[0.0.1]: https://github.com/SealtielFreak/ktree/releases/tag/Release
