from ktree.ntree import NTreeStatic

tree = NTreeStatic([(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)], 5)

tree.insert([0.1, 0.1, 0.1])
tree.insert([0.01, 0.2, 0.2])
tree.insert([0.01, 0.5, 0.1])
tree.insert([0.1, 0.025, 0.1])
tree.insert([0.1, 0.025, 0.1])

for nodes in tree.sort():
    print(nodes)
    print(nodes.data)
