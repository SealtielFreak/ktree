"""Compare NTreeStatic with NTreeDynamic on the same points."""

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
