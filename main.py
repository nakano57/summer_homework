from scipy.spatial import distance as sd
import numpy as np


class Node:
    def __init__(self, i: int, x=-1, y=-1):
        self.i = i
        self.x = np.random.rand()
        self.y = np.random.rand()

        if (x >= 0 and y >= 0):
            self.x = x
            self.y = y

        self.parent: Node = None
        self.children: list[Node] = []

    def __repr__(self):
        return "<i= %d, x= %f, y= %f, parent= %d, children= %s>" % (self.i, self.x, self.y, self.parent.i, self.children)


def distance(i: Node, j: Node):
    return sd.euclidean((i.x, j.x), (i.y, j.y))


def S(i: Node):
    l: list[Node] = []
    for j in nodes:
        if distance(i, j) <= 0.4:
            l.append(j)

    return l


def create_tree(root: Node):
    # Calculate the distance between the root and each nodes
    root_d = [distance(i, root) for i in nodes]

    # If the distance is greater than 0.4, then inf
    root_d = [i if i <= 0.4 else float('inf') for i in root_d]


if __name__ == '__main__':
    N = 11
    r = 0.4

    # Create Nodes
    nodes = []
    for i in range(N):
        nodes.append(Node(i))

    # Create Base Station
    BS = Node(-1, 0.5, 1.05)

    # Set root
    BS_d = [distance(i, BS) for i in nodes]
    root_index = BS_d.index(min(BS_d))
    nodes[root_index].parent = BS

    # Create Tree
    create_tree(nodes[root_index])
