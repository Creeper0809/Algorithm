import sys
from collections import Counter, defaultdict

def ntt(a, invert=False):
    mod = 998244353
    root = 3
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = pow(root, (mod - 1) // length, mod)
        if invert:
            wlen = pow(wlen, mod - 2, mod)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % mod
                a[j] = (u + v) % mod
                a[j + half] = (u - v + mod) % mod
                w = w * wlen % mod
        length <<= 1
    if invert:
        inv_n = pow(n, mod - 2, mod)
        for i in range(n):
            a[i] = a[i] * inv_n % mod

def convolution(a, b):
    mod = 998244353
    n = 1
    total = len(a) + len(b) - 1
    while n < total:
        n <<= 1
    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))
    ntt(fa, invert=False)
    ntt(fb, invert=False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % mod
    ntt(fa, invert=True)
    return fa[:total]

input = sys.stdin.readline
N = int(input())
A = list(map(int, input().split()))
B = list(map(int, input().split()))

cntA = Counter(A)
cntB = Counter(B)
maxA = max(cntA)
maxB = max(cntB)
maxS = maxA + maxB

T = int(N**0.5) + 1
heavyA = [v for v, c in cntA.items() if c > T]
heavyB = [v for v, c in cntB.items() if c > T]

heavy_extra = defaultdict(int)
for v in heavyA:
    for w in heavyB:
        extra = min(cntA[v], cntB[w]) - T
        if extra > 0:
            heavy_extra[v + w] += extra

base = [0] * (maxS + 1)
A_cnt = [0] * (maxA + 1)
B_cnt = [0] * (maxB + 1)
for v, c in cntA.items():
    A_cnt[v] = c
for v, c in cntB.items():
    B_cnt[v] = c

Ia = [0] * (maxA + 1)
Ib = [0] * (maxB + 1)
for t in range(1, T + 1):
    for v in range(maxA + 1):
        Ia[v] = 1 if A_cnt[v] >= t else 0
    for v in range(maxB + 1):
        Ib[v] = 1 if B_cnt[v] >= t else 0
    D = convolution(Ia, Ib)
    for s in range(min(len(D), maxS + 1)):
        base[s] += D[s]

bestX = 0
bestY = 0
for s, b in enumerate(base):
    total = b + heavy_extra.get(s, 0)
    if total > bestX or (total == bestX and s > bestY):
        bestX = total
        bestY = s

print(bestX, bestY)
