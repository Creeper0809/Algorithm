import sys
input = sys.stdin.readline
MOD = 10**9 + 7
factorial = [1] * (4000001)
for i in range(2,4000001):
    factorial[i] = (i * factorial[i-1]) % MOD

def power(x:int, y:int):
    res = 1
    x = x % MOD
    while y > 0:
        if y & 1:  # y가 홀수면
            res = res * x % MOD # x와 곱하고 나머지 연산
        # y가 짝수이면
        y = y >> 1  # y /= 2
        x = (x * x) % MOD  # 거듭제곱 계산
    return res

def ncr(n, r):
    B2 = power((factorial[r] * factorial[n-r]) % MOD ,MOD-2)
    return (factorial[n]*B2) % MOD

N = int(input())
for _ in range(N):
    n,r = map(int,input().split())
    print(ncr(n,r))

