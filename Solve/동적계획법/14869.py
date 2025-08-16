import sys
from collections import deque

input = sys.stdin.readline
INF = 10**9 + 7

n, m, s, e, t = map(int, input().split())
a = [[0] * (m + 1) for _ in range(n + 1)]
sum_ = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    line = list(map(int, input().split()))
    for j in range(1, m + 1):
        a[i][j] = line[j - 1]
        sum_[i][j] = sum_[i][j - 1] + a[i][j]
b = [0] * (n + 1)
for i in range(1, n + 1):
    b[i] = int(input())

dp = [[INF] * (n + 1) for _ in range(m + 1)]
mn = [[{'x': 0, 'v': INF} for _ in range(3)] for _ in range(m + 1)]
dq = [deque() for _ in range(n + 1)]

# 초기 mn[0] 설정: 가상 학원 0, 비용 -t
mn[0][0] = {'x': 0, 'v': -t}
mn[0][1] = {'x': 0, 'v': INF}
mn[0][2] = {'x': 0, 'v': INF}

def f(day, x):
    for k in range(3):
        if mn[day][k]['x'] != x and mn[day][k]['x'] != b[x]:
            return mn[day][k]['v']
    return INF

for i in range(1, m + 1):
    for j in range(1, n + 1):
        if i >= s:
            u = i - s
            now = f(u, j) - sum_[j][u]
            while dq[j] and dq[j][-1]['v'] >= now:
                dq[j].pop()
            dq[j].append({'x': u, 'v': now})
        while dq[j] and dq[j][0]['x'] < i - e:
            dq[j].popleft()
        if not dq[j] or dq[j][0]['v'] >= INF:
            dp[i][j] = INF
        else:
            dp[i][j] = dq[j][0]['v'] + t + sum_[j][i]
    # mn[i] 업데이트: top 3 최소
    mn_i = [{'x': 0, 'v': INF} for _ in range(3)]
    for j in range(1, n + 1):
        if dp[i][j] >= INF:
            continue
        val = dp[i][j]
        acad = j
        if val < mn_i[0]['v']:
            mn_i[2] = mn_i[1]
            mn_i[1] = mn_i[0]
            mn_i[0] = {'x': acad, 'v': val}
        elif val < mn_i[1]['v']:
            mn_i[2] = mn_i[1]
            mn_i[1] = {'x': acad, 'v': val}
        elif val < mn_i[2]['v']:
            mn_i[2] = {'x': acad, 'v': val}
    mn[i] = mn_i

# 답 계산: 마지막 세그먼트, +t 추가, j from max(0, m-e) to m-1
ans = INF
for i in range(1, n + 1):
    st = max(0, m - e)
    for j in range(st, m):
        now = f(j, i)
        if now >= INF:
            continue
        ans = min(ans, now + t + sum_[i][m] - sum_[i][j])
print(ans)