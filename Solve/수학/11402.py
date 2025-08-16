import sys
input = sys.stdin.readline

def power(x:int, y:int,m):
    res = 1
    x = x % m
    while y > 0:
        if y & 1:  # y가 홀수면
            res = res * x % m # x와 곱하고 나머지 연산
        # y가 짝수이면
        y = y >> 1  # y /= 2
        x = (x * x) % m  # 거듭제곱 계산
    return res

def ncr(n, r, m):
    facterial = [1] * (m)
    for i in range(1,m):
        facterial[i] = (i * facterial[i-1]) % m
    return (facterial[n] * power(facterial[r] * facterial[n-r],m-2,m)) % m

def lucas(n, r, p):
    if r > n:
        return 0
    result = 1
    while n or r:
        ni = n % p
        ri = r % p
        if ri > ni:
            return 0
        result = result * ncr(ni, ri, p) % p
        n //= p
        r //= p
    return result

n,r,m = map(int,input().split())
print(lucas(n,r,m))

