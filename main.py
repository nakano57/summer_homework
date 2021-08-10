from pyqubo import Array, Constraint, Placeholder, solve_qubo
from scipy.spatial import distance as sd
import numpy as np
import copy
import itertools as itr

import dotplot

N = 11
r = 0.4
alpha = 2.5


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


def u(T: int, i: Node) -> int:
    if i.parent.i == -1:
        return T

    return u(T, i.parent) - 1


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


def DVGA(N: list, f, T):
    Q = set()
    R = set(copy.copy(N))

    Y = set()
    x = np.zeros((len(N), T + 1))

    i = 0
    for i in range(1, T + 1):

        #Step 1
        for j in N:
            if u(T, j) == i:
                Y.add(j)

        #Step 2
        temp = set()
        for j in Y:
            temp = temp | set(j.children)

        if not (temp <= Q):
            w = 'failure'
            return None, None, w

        for j, k in itr.combinations(Y, 2):
            if f[j.i][k.i] == 1:
                w = 'failure'
                return None, None, w

        #Step 3
        V = set()
        for j in N:
            if set(C(j)) <= Q and (j in R):
                V.add(j)

        #Step 4
        # Solve MIS problem
        z_a = Array.create('z', shape=len(V), vartype='BINARY')

        H_A = sum(f[j.i][k.i] * z_a[list(V).index(j)] * z_a[list(V).index(k)]
                  for j, k in itr.combinations(V, 2))
        H_B = sum((((u(T, j) - i) / (u(T, j) - i - 1)) * z_a[list(V).index(j)])
                  for j in V)

        H = -H_A + alpha * H_B
        model = H.compile()
        qubo, offset = model.to_qubo()

        # Simurated Annealing
        raw_solution = solve_qubo(qubo)

        # Decode solution
        decoded_sample = model.decode_sample(raw_solution, vartype="BINARY")
        z = [decoded_sample.array('z', k) for k in range(len(V))]
        print(V, z)

        #Step4.1
        #Repeat Step 4 until we get the solution {zj} satisfying the constraints (16).
        #ToDo

        # Step 5
        V_0 = set()
        V_1 = set()
        for index, temp in enumerate(z):
            if temp == 0:
                V_0.add(list(V)[index])
            else:
                V_1.add(list(V)[index])

        # Step 6
        Q = Q | V_1
        R = R - V_1
        for j in N:
            if j in V_1:
                x[j.i][i] = 1
            else:
                x[j.i][i] = 0

        # Step 7
        #if R is empty, then False.
        if not R:
            #R is empty.
            if i <= T:
                T_u = i
                w = 'success'
            else:
                T_u = None
                w = 'failure'

        else:
            #R isn't empty.
            i += 1
            if i <= T:
                continue
            else:
                T_u = None
                w = 'failure'
        return x, T_u, w


def Computational_Method(N: list, f, T_star, K):
    T = len(N)
    k = 0
    X_u = None

    while True:
        X_hat_u, T_u, w = DVGA(N, f, T)
        if w == 'success':
            X_u = X_hat_u
            if T_u > T_star:
                T = T_u - 1
            else:
                break
        elif w == 'failure':
            k += 1
            if k >= K:
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
    for i, j in itr.combinations(nodes, 2):

        temp = S(p(i))
        temp.remove(i)
        temp2 = S(p(j))
        temp2.remove(j)

        if (j in temp) or (i in temp2):
            f[i.i][j.i] = 1
        else:
            f[i.i][j.i] = 0

    T = 15
    K = 2
    Computational_Method(nodes, f, T, K)
