from valid import valid
from grammar import CFG

prods = {
    'S': {'AM', 'AB'},
    'M': {'SB'},
    'A': {'a'},
    'B': {'b'}
}

cfg = CFG(prods)

print(valid(1, 4, 'aabb', cfg))
