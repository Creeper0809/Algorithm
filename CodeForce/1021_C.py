from itertools import product
from collections import deque


def generate_generators(n):
    gens = []

    def make_ops(l, r):
        m = r - l
        h = m // 2

        def opA(state):
            new = list(state)
            for i in range(h):
                new[l + i] = state[l + i] ^ state[l + h + i]
            return tuple(new)

        def opB(state):
            new = list(state)
            for i in range(h):
                new[l + h + i] = state[l + i] ^ state[l + h + i]
            return tuple(new)

        return opA, opB

    def add_nodes(l, r):
        m = r - l
        if m % 2 != 0:
            return
        A, B = make_ops(l, r)
        gens.extend([A, B])
        h = m // 2
        add_nodes(l, l + h)
        add_nodes(l + h, r)

    add_nodes(0, n)
    return gens


def reachable_set(s, gens):
    visited = {s}
    q = deque([s])
    while q:
        u = q.popleft()
        for g in gens:
            v = g(u)
            if v not in visited:
                visited.add(v)
                q.append(v)
    return visited


def rank_of_columns(s: str, n: int) -> int:
    p = n & -n
    L = n // p
    pivots = {}
    for r in range(L):
        m = 0
        idx = r
        for i in range(p):
            if s[idx] == '1':
                m |= 1 << i
            idx += L
        x = m
        while x:
            hb = x.bit_length() - 1
            if hb in pivots:
                x ^= pivots[hb]
            else:
                pivots[hb] = x
                break
    return len(pivots)


def compare_methods(n):
    gens = generate_generators(n)
    all_states = list(product([0, 1], repeat=n))
    reach_map = {s: reachable_set(s, gens) for s in all_states}
    mismatches = []
    for s in all_states:
        s_str = ''.join(map(str, s))
        for t in all_states:
            t_str = ''.join(map(str, t))
            brute = (t in reach_map[s])
            rank = (rank_of_columns(s_str, n) == rank_of_columns(t_str, n))
            if brute != rank:
                mismatches.append((s_str, t_str, brute, rank))
    return mismatches


if __name__ == "__main__":
    for n in [2, 4, 6]:
        mm = compare_methods(n)
        print(f"n = {n}, mismatches = {len(mm)}")
        if mm:
            print("Example mismatch:", mm[0])
