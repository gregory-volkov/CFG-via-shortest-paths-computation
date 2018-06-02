from itertools import product
import numpy as np
from shortest_path import shortest_paths


def implication(cfg, pi, scope):
    """
    Compute 2 sets of item implications
    :param cfg: CFG
    :param pi: PI set of items
    :param scope: pair of char indices of original string
    :return: 2 sets of pairs (2 due to 2 rules of implication), where each pair consists of 2 items
    """
    a, b = scope
    h_items = set()
    v_items = set()
    for nonterm, i_, j_ in pi:
        i = j_ + 1
        k = i - i_
        for j in range(i, b + 1):
            for to, fr in cfg.b[nonterm]:
                v_items.add(
                    (
                        (fr, i, j),
                        (to, i - k, j)
                    )
                )
        j = i_ - 1
        k = j_ - j
        for i in range(a, j + 1):
            for to, fr in cfg.c[nonterm]:
                h_items.add(
                    (
                        (fr, i, j),
                        (to, i, j + k)
                    )
                )

    return h_items, v_items


def valid(i, j, s, cfg):
    """
    Function VALID (Theorem 1)
    :param i: left border of string
    :param j: rght border of string
    :param s: string
    :param cfg: CFG
    :return: PI union IMPLIED
    """
    m = j - i + 1
    id2nonterm = dict(enumerate(cfg.nonterms))
    nonterm2id = {v: k for k, v in id2nonterm.items()}
    implied = set()

    # For m == 1 just returns items of the form (N, i, j) iff there is a rule N -> s[i - 1]
    # (i - 1) cause of min char index is 1, not 0
    if m == 1:
        return set((nonterm, i, j) for nonterm in cfg.term2nonterms[s[i - 1]])

    # Recursive call of VALID
    pi = valid(i, j - m // 2, s, cfg).union(valid(i + m // 2, j, s, cfg))

    # Computing implications
    h_items, v_items = implication(cfg, pi, (i, j))

    # Defining h and v - representation of lattice graph
    h = np.zeros((m, m, cfg.nonterm_n, cfg.nonterm_n), dtype=np.bool)
    v = np.zeros((m, m, cfg.nonterm_n, cfg.nonterm_n), dtype=np.bool)

    # Filling the lattice graph
    for fr, to in h_items:
        x, i1, j1 = fr
        a, i2, j2 = to
        h[j1 - i, j2 - i, nonterm2id[x], nonterm2id[a]] = True

    for fr, to in v_items:
        x, i1, j1 = fr
        a, i2, j2 = to
        v[i1 - i, i2 - i, nonterm2id[x], nonterm2id[a]] = True

    # Defining subarray of V (cause of source node is in the middle of graph)
    subarray_size = m // 2 + 1
    sub_v = np.zeros((subarray_size, subarray_size, cfg.nonterm_n, cfg.nonterm_n), dtype=np.bool)

    for i_, j_ in product(range(subarray_size - 1), repeat=2):
        sub_v[i_ + 1, j_ + 1] = v[i_, j_]

    # Calling shortest path for subarray of original graph (cause of source node is in the middle of graph)
    dist = shortest_paths(subarray_size, h[-subarray_size:, -subarray_size:], sub_v)

    # Computing the set IMPLIED
    for i_, j_ in product(range(subarray_size), repeat=2):
        for nonterm_id_1, nonterm_id_2 in product(range(cfg.nonterm_n), repeat=2):
            if dist[i_, j_, nonterm_id_1, nonterm_id_2]:
                x, a = id2nonterm[nonterm_id_1], id2nonterm[nonterm_id_2]
                if x in cfg.term2nonterms[s[i + m // 2 - 2]]:
                    implied.add((a, i + i_ - 1, j - (subarray_size - j_) + 1))

    return pi.union(implied)
