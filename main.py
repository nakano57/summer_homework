from scipy.spatial import distance as sd
import numpy as np
import copy

import dotplot

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

        self.root = False

    def __repr__(self):
        #return "<i= %d, x= %f, y= %f, parent= %s, children= %s>" % (
        #    self.i, self.x, self.y, self.parent, self.children)
        return "<i= %d>" % (self.i)


def distance(i: Node, j: Node):
    return sd.euclidean((i.x, i.y), (j.x, j.y))


# the set of nodes j∈N where d(i,j)≤r
def S(i):
    l: list[Node] = []

    if type(i) == list:
        for j in i:
            l += S(j)
    else:
        for j in nodes:
            if distance(i, j) <= r:
                l.append(j)

    return l


def p(i: Node):
    return i.parent


def C(j: Node):
    return j.children


#Prim's algorithm
def create_tree(root: Node):

    not_check = copy.copy(nodes)
    not_check.remove(root)
    confirmed = [root]

    while True:
        # node, distance , parent
        min_distance_node = (Node, float('inf'), Node)
        temp = (Node, float('inf'), Node)

        for n in confirmed:
            # Calculate the distance between the confirmed node and each nodes
            # If the distance is greater than r, then inf
            not_check.sort(key=lambda x: (distance(x, n) if distance(x, n) <= r
                                          else float('inf')))
            #print(n.i, not_check)

            # ---for Debug---
            # ds = [distance(i, n) for i in not_check]
            # ds = [i if i <= r else float('inf') for i in ds]
            # print(ds)
            # ---------------

            ds = (distance(not_check[0], n)
                  if distance(not_check[0], n) <= r else float('inf'))

            temp = (not_check[0], ds, n)

            if temp[1] < min_distance_node[1]:
                min_distance_node = copy.copy(temp)

        confirmed.append(min_distance_node[0])
        try:
            not_check.remove(min_distance_node[0])
        except ValueError as e:
            print(e)
            print('cant make a tree')
            exit(1)
        min_distance_node[0].parent = min_distance_node[2]
        min_distance_node[2].children.append(min_distance_node[0])
        V[min_distance_node[2].i][min_distance_node[0].i] = 1
        V[min_distance_node[0].i][min_distance_node[2].i] = 1

        if not not_check:
            break


def GreedyAlgorithm(N: list, F):
    Q = set()
    R = set(copy.copy(N))

    V = set()

    for j in N:
        if set(j.children) <= Q and j in R:
            V.add(j)

    print(V)
    #Solve MIS problem


if __name__ == '__main__':

    # Create Nodes
    nodes = []
    for i in range(N):
        nodes.append(Node(i))

    # Create Base Station
    BS = Node(-1, 0.5, 1.05)

    # Set root
    BS_d = [distance(i, BS) for i in nodes]
    if min(BS_d) > r:
        print("Error: Base Station is out of range")
        exit(1)

    root_index = BS_d.index(min(BS_d))
    nodes[root_index].parent = BS
    nodes[root_index].root = True

    # Create Tree
    V = np.zeros((N, N))
    create_tree(nodes[root_index])
    #print(V)
    dotplot.plot(nodes, V, BS)

    #Create interference matrix
    f = np.zeros((N, N))
    for i in nodes:
        for j in nodes:
            if i == j:
                continue

            temp = S(p(i))
            temp.remove(i)
            temp2 = S(p(j))
            temp2.remove(j)

            if (j in temp) or (i in temp2):
                f[i.i][j.i] = 1
            else:
                f[i.i][j.i] = 0

    GreedyAlgorithm(nodes, f)
