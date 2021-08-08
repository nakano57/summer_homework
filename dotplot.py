import matplotlib.pyplot as plt


def plot(nodes, V, BS):
    plt.figure()
    plt.xlim((-0.1, 1.1))
    plt.ylim((-0.1, 1.1))

    plt.scatter(BS.x, BS.y, color='r')
    plt.annotate('BS', xy=(BS.x, BS.y))

    for n in nodes:
        if n.root:
            plt.plot([BS.x, n.x], [BS.y, n.y], color='r')
            break

    for n in nodes:
        plt.scatter(n.x, n.y)
        plt.annotate(str(n.i), xy=(n.x, n.y))

    for i in range(len(V)):
        for j in range(i):
            if V[i][j] == 1:
                plt.plot([nodes[i].x, nodes[j].x], [nodes[i].y, nodes[j].y])

    plt.savefig("tree.jpg")
    #plt.show()
