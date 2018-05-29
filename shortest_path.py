import numpy as np
from relation import Relation


# dist is a list of relations
# h and v - matrices
def single_edge_extend(dist, lattice_graph):
    h, v = lattice_graph
    dist += (dist.T.dot(v)).T + dist.dot(h)


def shortest_paths_algo(lattice_graph, corners, dist):
    h, v = lattice_graph
    x, y = corners
    i1, j1 = x
    i2, j2 = y
    size = i1 - i2 + 1
    if size == 1:
        for j, rel in enumerate(h[j1]):
            dist[i1, j] += dist[i1, j1] * rel

        for i, rel in enumerate(v[i1]):
            dist[i, j1] += dist[i1, j1] * v[i1, i]

        return

    mid = size // 2
    a_corners = (x, (i2 + mid, j2 - mid))
    shortest_paths_algo(lattice_graph, a_corners, dist)

    single_edge_extend(dist, lattice_graph)

    b_corners = ((i1 - mid, j1), (i2, j2 - mid))
    shortest_paths_algo(lattice_graph, b_corners, dist)

    d_corners = ((i1, j1 + mid), (i2 + mid, j2))
    shortest_paths_algo(lattice_graph, d_corners, dist)

    single_edge_extend(dist, lattice_graph)

    c_corners = ((i1 - mid, j1 + mid), y)
    shortest_paths_algo(lattice_graph, c_corners, dist)


def shortest_paths(n, h, v):
    dist = np.array(
        [[Relation() for _ in range(n)] for _ in range(n)]
    )

    dist[-1] = h[0]
    dist[:, 0] = v[-1]

    shortest_paths_algo((h, v), ((n - 1, 0), (0, n - 1)), dist=dist)

    return dist
