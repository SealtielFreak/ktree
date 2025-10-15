from ktree.ntree import NTree

tree = NTree([(0, 10)], 2)

tree.insert([2])
tree.insert([1])
tree.insert([2])
tree.insert([9])

for nodes in tree.sort():
    print(nodes)
    print(nodes.data)
