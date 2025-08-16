import math
import random


n = int(input())

basic_primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41}


def power(x, y, p):
    res = 1
    x = x % p
    while y > 0:
        if y & 1:  # y가 홀수면
            res = res * x % p  # x와 곱하고 나머지 연산
        # y가 짝수이면
        y = y >> 1  # y /= 2
        x = (x * x) % p  # 거듭제곱 계산
    return res


# 밀러-라빈 판정
def miller_rabin(n, a):
    d = n - 1  # 홀수
    while d % 2 == 0:
        d //= 2  # 2^d*r+1

    x = power(a, d, n)  # a^{d} % n 계산

    if x == 1 or x == n - 1:  # x가 1 또는 n-1이면 소수
        return True
    while d != n - 1:  # n-1이 아닌 동안
        x = power(x, 2, n)  # x^{2} % n 계산
        d *= 2
        # x가 1이면 합성수이고 아니면 소수
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False


def isPrime(n):
    if n in basic_primes:  # 기본적으로 소수인 경우
        return True
    if n == 1 or n % 2 == 0:  # 1과 2의 배수는 소수가 아님
        return False
    for a in basic_primes:
        # long long 범위는 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41의 소수로 검사.
        # 37까지만 검사해도 됨
        # 성립하지 않아 false를 반환하면 아마도 소수가 아님 (not False = True)
        if not miller_rabin(n, a):
            return False

    return True

def f(x,c,n):
    return (x**2 + c) % n

def pollads_ro(n):
    # 1은 소수가 아님
    if n == 1:
        return 1
    # 2를 제외한 모든 짝수는 합성수에 해당
    if n % 2 == 0:
        return 2
    # 이미 소수라면 소인수에 해당
    if isPrime(n):
        return n
    x = random.randrange(2,n)
    c = random.randrange(1,n)
    y = x
    g = 1
    # gcd != 1 소인수일 가능성이 있음
    # gcd(x-y,n) = gcd(30,81) = 3 즉 결정론적인 함수를 돌아서 나온 함숫값하고 최소공배수를 뽑았을 때
    # gcd 값이 1이 아니면 어쨋든 gcd 값인 인수는 있다는것 이게 소수이면 소인수
    while g == 1:
        # 폴라드 로의 자명한 결정론적 함수(x^2 + c)로 두개의 포인터 생성
        # x는 f(x) y=f(f(y)) 이렇게하면 속도가 다른 두개의 포인터가 사이클이 있는 결정론적 함수를 돌게 됨
        x = f(x,c,n)
        y = f(f(y,c,n),c,n)
        g = math.gcd(x-y,n)
        # g == n이라는 뜻은 x == y 라는뜻 두개의 포인터가 충돌했다는 뜻은 아마도 소인수에 해당하는 부분이 없다는것
        # 다시 폴라드-로 알고리즘을 돌 것
        if g == n:
            return pollads_ro(n)
    # 만약 g의 값이 1이 아니라면 예를 들어 8이라면 2로 한번 더 나눠짐으로(소수가 아님으로) 폴라드-로 알고리즘을 g의 값으로 돌기
    if not isPrime(g):
        return pollads_ro(g)
    return g

res = n
while n > 1:
    p = pollads_ro(n)
    if n % p != 0:
        continue
    # n의 소인수를 찾았으면 n%p 즉 소인수로 나눠지는 만큼 나눔
    # 이는 피 함수를 계산할때 한번만 계산하기 위함
    while n % p == 0:
        n //= p
    res = res - res//p
print(int(res))