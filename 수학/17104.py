import sys
input = sys.stdin.readline

mod = 998244353
root = 3

def modexp(a, e):
    r = 1
    while e:
        if e & 1:
            r = r * a % mod
        a = a * a % mod
        e >>= 1
    return r

def ntt(a, invert):
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
        wlen = modexp(root, (mod - 1) // length)
        if invert:
            wlen = modexp(wlen, mod - 2)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % mod
                a[j] = (u + v) % mod
                a[j + half] = (u - v) % mod
                w = w * wlen % mod
        length <<= 1
    if invert:
        inv_n = modexp(n, mod - 2)
        for i in range(n):
            a[i] = a[i] * inv_n % mod

def convolution(a, b):
    n1 = len(a)
    n2 = len(b)
    n = 1
    while n < n1 + n2 - 1:
        n <<= 1
    fa = a + [0] * (n - n1)
    fb = b + [0] * (n - n2)
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % mod
    ntt(fa, True)
    return fa

t = int(input())
s = [int(input()) for _ in range(t)]
maxN = 1000
A = [1] * (maxN + 1)
A[0] = A[1] = 0
for i in range(2, int(maxN**0.5) + 1):
    if A[i]:
        for j in range(i * i, maxN + 1, i):
            A[j] = 0
C = convolution(A, A)
out = []
for N in s:
    cnt = C[N]
    if N % 2 == 0 and A[N // 2]:
        cnt += 1
    out.append(str(cnt // 2))
sys.stdout.write("\n".join(out))
