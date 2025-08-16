import sys

def factorize(k):
    factors = {}
    # 2로 나누기
    while k % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        k //= 2
    # 3,5,7,... 으로 나누기
    p = 3
    while p * p <= k:
        while k % p == 0:
            factors[p] = factors.get(p, 0) + 1
            k //= p
        p += 2
    # 남은 소수
    if k > 1:
        factors[k] = factors.get(k, 0) + 1
    return factors

def exp_in_factorial(n, p):
    cnt = 0
    while n:
        n //= p
        cnt += n
    return cnt

def gcd_factorial(n, k):
    k_facs = factorize(k)
    g = 1
    for p, a in k_facs.items():
        e = exp_in_factorial(n, p)
        if e > 0:
            g *= p ** min(a, e)
    return g


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    n, k = map(int, line.split())
    print(gcd_factorial(n, k))