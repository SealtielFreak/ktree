import random

from ktree.ntree import NTreeDynamic

N_DIMENSION = 3

random.seed(0)

tree = NTreeDynamic(1)

for _ in range(5):
    tree.insert([random.randint(0, 64) for _ in range(N_DIMENSION)])

sorted_data = tree.sort()
l_sorted_data = 0

for shape, data in sorted_data:
    print("Shape:", shape)
    print(len(data), data)

    l_sorted_data += len(data)

print(l_sorted_data)
print(tree.shape)
