import sys


def solve():
    n = int(sys.stdin.readline())
    mod = 1000000007

    phi = [i for i in range(n + 1)]
    for i in range(2, n + 1):
        if phi[i] == i:
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i


    sum_d_phi_d = [0] * (n + 1)
    for d in range(1, n + 1):
        term = (d * phi[d]) % mod
        for k in range(d, n + 1, d):
            sum_d_phi_d[k] = (sum_d_phi_d[k] + term) % mod

    ans = 0

    inv2 = (mod + 1) // 2

    for j in range(2, n + 1):
        f_j = sum_d_phi_d[j]
        sum_lcm_ij = (j * ((1 + f_j) % mod)) % mod
        sum_lcm_ij = (sum_lcm_ij * inv2) % mod
        term_j = (sum_lcm_ij - j + mod) % mod
        ans = (ans + term_j) % mod

    print(ans)


solve()