from collections import defaultdict


class CFG(object):

    # A -> BC
    # c['C'] = {(A, B)}
    # b['B'] = {(A, C)}
    def __init__(self, prods):
        self.nonterms = set()
        self.terms = set()
        self.term2nonterms = defaultdict(set)
        self.c = defaultdict(set)
        self.b = defaultdict(set)
        for lp in prods:
            self.nonterms.add(lp)
            for rp in prods[lp]:
                if len(rp) == 1:
                    self.term2nonterms[rp].add(lp)
                    self.terms.add(rp)
                else:
                    self.b[rp[0]].add((lp, rp[1]))
                    self.c[rp[1]].add((lp, rp[0]))
