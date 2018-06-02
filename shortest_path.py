import numpy as np


def matrix_mul(a, b):
    """
    Multiplication of 2 matrices, where matrix element is boolean matrix (representation of binary relation)
    :param a: 1 matrix
    :param b: 1 matrix
    :return: result of mul
    """
    n = a.shape[0]
    s = a.shape[2]
    res = np.zeros((n, n, s, s), dtype=np.bool)
    for i in range(n):
        for j in range(n):
            for term in range(n):
                res[i, j] = res[i, j] + a[i, term].dot(b[term, j])
    
    return res


def transpose(x):
    """
    Transposition of matrix, where matrix element is boolean matrix
    :param x: matrix
    :return: result of transposition
    """
    return np.transpose(x, axes=(1, 0, 2, 3))


def single_edge_extend(dist, lattice_graph):
    """
    Operation SingleEdgeExtend, described in Lemma 3
    :param dist: DIST matrix
    :param lattice_graph: pair of 2 matrices: H and V
    :return: None (changes DIST matrix)
    """
    h, v = lattice_graph
    dist += transpose(matrix_mul(transpose(dist), v)) + matrix_mul(dist, h)


def shortest_paths_algo(lattice_graph, corners, dist):
    """

    :param lattice_graph: pair of 2 matrices: H and V
    :param corners: left upper and lower right coordinates of current quadrant
    :param dist: DIST matrix
    :return: None (changes DIST matrix)
    """
    h, v = lattice_graph
    x, y = corners
    i1, j1 = x
    i2, j2 = y
    size = i1 - i2 + 1

    if size == 1:
        for j, rel in enumerate(h[j1]):
            dist[i1, j] += dist[i1, j1].dot(rel)

        for i, rel in enumerate(v[i1]):
            dist[i, j1] += dist[i1, j1].dot(v[i1, i])

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
    """
    ShortestPaths algorithm, described in proof of Lemma 1
    :param n: size of graph
    :param h: H matrix
    :param v: V matrix
    :return: DIST matrix
    """
    s = h.shape[2]
    dist = np.zeros((n, n, s, s), dtype=np.bool)

    dist[-1] = h[0]
    dist[:, 0] = v[-1]

    shortest_paths_algo((h, v), ((n - 1, 0), (0, n - 1)), dist=dist)

    return dist
