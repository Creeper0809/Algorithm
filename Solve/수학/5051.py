import sys

input = sys.stdin.readline

MOD = 998244353
PRIMITIVE_ROOT = 3


# fast exponentiation
def modpow(x, e, m=MOD):
    r = 1
    while e:
        if e & 1:
            r = r * x % m
        x = x * x % m
        e >>= 1
    return r


# in-place iterative NTT
def ntt(a, invert):
    n = len(a)
    # bit-reverse
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    # layers
    length = 2
    while length <= n:
        wlen = modpow(PRIMITIVE_ROOT, (MOD - 1) // length)
        if invert:
            wlen = modpow(wlen, MOD - 2)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v + MOD) % MOD
                w = w * wlen % MOD
        length <<= 1
    # if inverse, divide by n
    if invert:
        inv_n = modpow(n, MOD - 2)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


# 입력
n = int(input().strip())

# 1) f[r]: a^2 ≡ r (mod n) 의 빈도
f = [0] * n
for a in range(1, n):
    f[(a * a) % n] += 1

# 2) 순환 합성곱을 위한 NTT
M = 1
while M < 2 * n:
    M <<= 1

A = f + [0] * (M - n)
ntt(A, False)
for i in range(M):
    A[i] = A[i] * A[i] % MOD
ntt(A, True)

# 3) g[s]: a^2 + b^2 ≡ s (mod n) 인 순서쌍 개수
g = [0] * n
for i in range(M):
    g[i % n] = (g[i % n] + A[i])  # 값이 이미 정확히 저장됨

# 4) a ≤ b 보정 후 답 계산
sum1 = 0
sum2 = 0
for s in range(n):
    sum1 += f[s] * g[s]
    sum2 += f[s] * f[(2 * s) % n]

ans = (sum1 + sum2) // 2
print(ans)
