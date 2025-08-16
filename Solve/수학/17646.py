import math
import random
import sys
from random import randrange
from math import gcd
input = sys.stdin.readline

# 소수 후보
basic_primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41}

# 모듈러 거듭 제곱
def mod_pow(base, exponent, mod):
    result = 1
    base %= mod
    while exponent:
        if exponent & 1:
            result = result * base % mod
        base = base * base % mod
        exponent >>= 1
    return result

# 소수 판별 (Miller-Rabin)
is_prime_memo = dict()

def is_prime(n):
    if n in is_prime_memo:
        return is_prime_memo[n]
    if n == 1:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    if n in basic_primes:
        is_prime_memo[n] = True
        return True

    def miller_rabin_test(n, a):
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return True
        return False

    is_probably_prime = True
    for base in basic_primes:
        if not miller_rabin_test(n, base):
            is_probably_prime = False
            break

    is_prime_memo[n] = is_probably_prime
    return is_probably_prime

# Pollard's Rho 알고리즘
factor_memo = dict()

def pollards_rho(n):
    if n == 1:
        return 1
    if n % 2 == 0:
        return 2
    if is_prime(n):
        return n

    def f(x, c, mod):
        return (x ** 2 + c) % mod

    x = random.randrange(2, n)
    c = random.randrange(1, n)
    y = x
    g = 1

    while g == 1:
        x = f(x, c, n)
        y = f(f(y, c, n), c, n)
        g = math.gcd(x - y, n)
        if g == n:
            return pollards_rho(n)
    if not is_prime(g):
        return pollards_rho(g)
    return g


# 정수 n의 소인수분해 리스트 반환
def factorize(n):
    if n in factor_memo:
        return factor_memo[n]
    if n == 1:
        factor_memo[n] = []
        return []
    if n % 2 == 0:
        factor_memo[n] = [2] + factorize(n // 2)
        return factor_memo[n]
    if is_prime(n):
        factor_memo[n] = [n]
        return [n]
    p = pollards_rho(n)
    factor_memo[n] = factorize(p) + factorize(n // p)
    return factor_memo[n]


# 제곱근 계산 (제곱수만)
def integer_sqrt(n):
    prime_factors = factorize(n)
    factors = {}
    for p in prime_factors:
        factors[p] = factors.get(p, 0) + 1
    result = 1
    for p, count in factors.items():
        result *= pow(p, count // 2)
    return result

# Tonelli-Shanks 알고리즘 (mod p에서 제곱근)
def tonelli_shanks(p):
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = randrange(2, p)
    while pow(z, (p - 1) // 2, p) == 1:
        z = randrange(2, p)
    m, c = s, pow(z, q, p)
    t, r = pow(p - 1, q, p), pow(p - 1, (q + 1) // 2, p)
    while t != 1 and t != 0:
        i, temp = 0, t
        while temp % p != 1:
            temp = pow(temp, 2, p)
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = (b * b) % p
        t = (t * c) % p
        r = r * b % p
    return r

# Cornacchia 알고리즘
def cornacchia(p):
    if p % 4 == 3:
        return False
    if p == 2:
        return 1
    r = tonelli_shanks(p)
    a = p
    while r * r > p:
        a, r = r, a % r
    return r

# 네 제곱수 정리 기반 항 개수 판단
def min_square_count(n):
    factors = {}
    for f in factorize(n):
        factors[f] = factors.get(f, 0) + 1

    all_even = True
    for exp in factors.values():
        if exp % 2 != 0:
            all_even = False
            break

    legendre_ok = True
    for p, exp in factors.items():
        if p % 4 == 3 and exp % 2 != 0:
            legendre_ok = False
            break

    if all_even:
        return 1
    if legendre_ok:
        return 2
    while n % 4 == 0:
        n //= 4
    return 3 if n % 8 != 7 else 4

def get_case_1(n):
    return [integer_sqrt(n)]

def get_case_2(n):
    factors = factorize(n)
    factor_counts = {}
    for f in factors:
        factor_counts[f] = factor_counts.get(f, 0) + 1

    common_factor = 1
    odd_primes = []
    for p, exp in factor_counts.items():
        common_factor *= pow(p, exp // 2)
        if exp % 2:
            odd_primes.append(p)

    result = [1, 0]
    for p in odd_primes:
        x = cornacchia(p)
        y = integer_sqrt(p - x * x)
        a, b = result
        result = [a * y + b * x, abs(a * x - b * y)]
    return [x * common_factor for x in result]

def get_case_3(n):
    factors = factorize(n)
    factor_counts = {}
    for f in factors:
        factor_counts[f] = factor_counts.get(f, 0) + 1

    common_factor = 1
    reduced_n = 1
    for p, exp in factor_counts.items():
        common_factor *= pow(p, exp // 2)
        reduced_n *= pow(p, exp % 2)

    t = 1
    while min_square_count(reduced_n - t * t) != 2:
        t += 1
    return [x * common_factor for x in get_case_2(reduced_n - t * t)] + [t * common_factor]

def get_case_4(n):
    pow_of_4 = 0
    while n % 4 == 0:
        n //= 4
        pow_of_4 += 1
    base_case = get_case_3(n - 1)
    scale = 2 ** pow_of_4
    return [x * scale for x in base_case] + [scale]

# 실행부
n = int(input())
count = min_square_count(n)
print(count)
if count == 1:
    print(*get_case_1(n))
elif count == 2:
    print(*get_case_2(n))
elif count == 3:
    print(*get_case_3(n))
else:
    print(*get_case_4(n))
