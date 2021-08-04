from scipy.spatial import distance as sd
import numpy as np
import copy

N = 11
r = 0.4


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
        #return "<i= %d, x= %f, y= %f, parent= %s, children= %s>" % (
        #    self.i, self.x, self.y, self.parent, self.children)
        return "<i= %d>" % (self.i)


def distance(i: Node, j: Node):
    return sd.euclidean((i.x, i.y), (j.x, j.y))


# the set of nodes j∈N where d(i,j)≤r
def S(i: Node):
    l: list[Node] = []
    for j in nodes:
        if distance(i, j) <= 0.4:
            l.append(j)

    return l


def create_tree(root: Node):

    not_check = copy.copy(nodes)
    not_check.remove(root)
    confirmed = [root]

    while True:
        # node, distance , parent
        min_distance_node = (None, float('inf'), None)

        for n in confirmed:
            # Calculate the distance between the confirmed node and each nodes
            # If the distance is greater than 0.4, then inf
            not_check.sort(key=lambda x: (distance(x, n) if distance(x, n) <= r
                                          else float('inf')))
            #print(n.i, not_check)

            #ds = [distance(i, n) for i in not_check]
            #ds = [i if i <= r else float('inf') for i in ds]
            #print(ds)

            temp = (not_check[0], distance(not_check[0], n), n)

            if temp[1] < min_distance_node[1]:
                min_distance_node = copy.copy(temp)

        confirmed.append(min_distance_node[0])
        not_check.remove(min_distance_node[0])

        min_distance_node[0].parent = min_distance_node[2]
        min_distance_node[2].children.append(min_distance_node[0])
        V[min_distance_node[2].i][min_distance_node[0].i] = 1
        V[min_distance_node[0].i][min_distance_node[2].i] = 1
        #print(V)

        if not not_check:
            break


if __name__ == '__main__':

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
    V = np.zeros((N, N))
    create_tree(nodes[root_index])
    print(V)
