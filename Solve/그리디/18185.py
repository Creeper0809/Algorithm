import sys

input = sys.stdin.readline

n = int(input())
B = 3
C = 2
v = list(map(int, input().split()))
a = [0] * n
b = [0] * n

ans = 0

if B <= C:
    ans = sum(v) * B
else:
    for i in range(n):
        ans += v[i] * B
        a[i] = v[i]
        v[i] = 0

        if i + 1 < n:
            temp = min(a[i], v[i + 1])
            ans += temp * C
            a[i] -= temp
            v[i + 1] -= temp
            b[i] += temp

        if i - 1 >= 0 and i + 1 < n:
            temp = min(b[i - 1], v[i + 1])
            ans += temp * C
            v[i + 1] -= temp

print(ans)