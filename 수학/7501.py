import math
import random
basic_primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41}


def power(x, y, p):
    res = 1
    x = x % p
    while y > 0:
        if y & 1:
            res = res * x % p
        y = y >> 1  # y /= 2
        x = (x * x) % p
    return res

def miller_rabin(n, a):
    d = n - 1
    while d % 2 == 0:
        d //= 2

    x = power(a, d, n)

    if x == 1 or x == n - 1:
        return True
    while d != n - 1:
        x = power(x, 2, n)
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False


def isPrime(n):
    if n in basic_primes:  # 기본적으로 소수인 경우
        return True
    if n == 1 or n % 2 == 0:
        return False
    for a in basic_primes:
        if not miller_rabin(n, a):
            return False

    return True

def f(x,c,n):
    return (x**2 + c) % n

def pollads_ro(n):
    if n == 1:
        return 1
    if n % 2 == 0:
        return 2
    if isPrime(n):
        return n
    x = random.randrange(2,n)
    c = random.randrange(1,n)
    y = x
    g = 1
    while g == 1:
        x = f(x,c,n)
        y = f(f(y,c,n),c,n)
        g = math.gcd(x-y,n)
        if g == n:
            return pollads_ro(n)
    if not isPrime(g):
        return pollads_ro(g)
    return g

def factorial_mod(n, mod):
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % mod
        if result >= mod:
            return result
    return result

A, B = map(int, input().split())
answer = []
for K in range(A, B + 1):
    if K in {1,9}:
        answer.append(K)
        continue
    if K % 2 == 0:
        continue  # 짝수는 제외
    if isPrime(K):
        answer.append(K)
print(*answer)