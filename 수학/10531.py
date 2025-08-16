MOD = 998244353
PRIMITIVE_ROOT = 3

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            for j in range(length // 2):
                u = a[i + j]
                v = a[i + j + length // 2] * w % MOD
                a[i + j] = (u + v) % MOD
                a[i + j + length // 2] = (u - v + MOD) % MOD
                w = w * wlen % MOD
        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def ntt_convolution(a, b):
    n = 1
    while n < len(a) + len(b):
        n <<= 1
    a += [0] * (n - len(a))
    b += [0] * (n - len(b))

    ntt(a, False)
    ntt(b, False)
    for i in range(n):
        a[i] = a[i] * b[i] % MOD
    ntt(a, True)
    return a

N = int(input())
a = [int(input()) for _ in range(N)]
size = (max(a)+1)
a_count = [0] * size

for i in a:
    a_count[i] += 1


c = ntt_convolution(a_count[:], a_count[:])
M = int(input())
answer = 0
for _ in range(M):
    number = int(input())
    if (len(c) > number and c[number] > 0) or (size > number and a_count[number] > 0):
        answer += 1
print(answer)