import sys
from collections import defaultdict, deque
input = sys.stdin.readline
N, K = map(int, input().split())
A = list(map(int, input().split()))
M = int(input())
queries = []
for i in range(M):
    l, r = map(int, input().split())
    queries.append((l-1, r, i))
prefix_sum = [0] * (N + 1)
for i in range(N):
    prefix_sum[i + 1] = prefix_sum[i] + A[i]
block = int((N + 1) ** 0.5) + 1
queries.sort(key=lambda x: (x[0] // block, x[1] if (x[0] // block) % 2 == 0 else -x[1]))
freq = defaultdict(deque)
dist_count = defaultdict(int)
current_max = 0
def update_dist(v):
    dq = freq[v]
    return dq[-1] - dq[0] if len(dq) >= 2 else 0
def add(idx):
    global current_max
    v = prefix_sum[idx] % K
    old = update_dist(v)
    if old > 0:
        dist_count[old] -= 1
    dq = freq[v]
    if not dq or idx > dq[-1]:
        dq.append(idx)
    else:
        dq.appendleft(idx)
    new = update_dist(v)
    if new > 0:
        dist_count[new] += 1
        current_max = max(current_max, new)
def remove(idx):
    global current_max
    v = prefix_sum[idx] % K
    old = update_dist(v)
    if old > 0:
        dist_count[old] -= 1
    dq = freq[v]
    if dq and dq[0] == idx:
        dq.popleft()
    else:
        dq.pop()
    new = update_dist(v)
    if new > 0:
        dist_count[new] += 1
    while current_max > 0 and dist_count[current_max] == 0:
        current_max -= 1
res = [0] * M
L, R = 0, -1
for ql, qr, qi in queries:
    while L > ql:
        L -= 1
        add(L)
    while R < qr:
        R += 1
        add(R)
    while L < ql:
        remove(L)
        L += 1
    while R > qr:
        remove(R)
        R -= 1
    res[qi] = current_max
print('\n'.join(map(str, res)))