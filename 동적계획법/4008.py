import sys
from collections import deque

input = sys.stdin.readline

n = int(input())
A, B, C = map(int, input().split())
xs = list(map(int, input().split()))

P = [0] * (n + 1)
for i in range(1, n + 1):
    P[i] = P[i - 1] + xs[i - 1]

dp = [0] * (n + 1)
dq = deque()
dq.append((0, 0))  # (slope m, intercept b)

for i in range(1, n + 1):
    X = P[i]
    while len(dq) >= 2 and dq[0][0] * X + dq[0][1] <= dq[1][0] * X + dq[1][1]:
        dq.popleft()
    best = dq[0][0] * X + dq[0][1]
    dp[i] = A * X * X + B * X + C + best

    M = P[i]
    m = -2 * A * M
    b = dp[i] + A * M * M - B * M

    while len(dq) >= 2:
        m1, b1 = dq[-2]
        m2, b2 = dq[-1]
        if (b - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m):
            dq.pop()
        else:
            break
    dq.append((m, b))

print(dp[n])
