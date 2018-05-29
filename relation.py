from semiring import Semiring
from itertools import product


class Relation(Semiring):

    def __init__(self, rel=None):
        self.rel = set() if rel is None else rel

    def __add__(self, other):
        new_rel = Relation()
        new_rel.rel = self.rel.union(other.rel)
        return new_rel

    def __mul__(self, other):
        new_rel = Relation()
        new_rel.rel = set()
        for i, j in product(self.rel, other.rel):
            if i[1] == j[0]:
                new_pair = (i[0], j[1])
                new_rel.rel.add(new_pair)
        return new_rel

    def __repr__(self):
        return str(self.rel) if self.rel else "{}"
