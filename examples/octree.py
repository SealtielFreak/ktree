from ktree.ntree import NTree

tree = NTree([(0., 1.), (0., 1.), (0., 1.)], 5)

tree.insert([.1, .1, .1])
tree.insert([.01, .2, .2])
tree.insert([.01, .5, .1])
tree.insert([.1, .025, .1])
tree.insert([.1, .025, .1])

for nodes in tree.sort():
    print(nodes)
    print(nodes.data)
