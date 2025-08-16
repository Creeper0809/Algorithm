import sys

input = sys.stdin.readline

MOD =  99991


def modexp(a, e, mod=MOD):
    r = 1
    a %= mod
    while e:
        if e & 1:
            r = r * a % mod
        a = a * a % mod
        e >>= 1
    return r


N, K = map(int, input().split())
S = list(map(int, input().split()))

sqrt5 = modexp(5, (MOD + 1) // 4)
inv_sqrt5 = modexp(sqrt5, MOD - 2)
inv2 = (MOD + 1) // 2

alpha = (1 + sqrt5) * inv2 % MOD
beta = (1 - sqrt5) * inv2 % MOD

dp_a = [0] * (K + 1)
dp_b = [0] * (K + 1)
dp_a[0] = dp_b[0] = 1

for s in S:
    a_s = modexp(alpha, s)
    b_s = modexp(beta, s)
    for k in range(K, 0, -1):
        dp_a[k] = (dp_a[k] + dp_a[k - 1] * a_s) % MOD
        dp_b[k] = (dp_b[k] + dp_b[k - 1] * b_s) % MOD

ans = (dp_a[K] - dp_b[K]) * inv_sqrt5 % MOD
print(ans)