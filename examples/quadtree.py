from ktree.ntree import NTree

tree = NTree([(0., 1.), (0., 1.)], 2)

tree.insert([0.1, 0.1])
tree.insert([0.01, 0.2])
tree.insert([0.01, 0.5])

for nodes in tree.sort():
    print(nodes)
    print(nodes.data)
