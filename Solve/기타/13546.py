import sys
from collections import defaultdict, deque

input = sys.stdin.readline

N, K = map(int, input().split())
arr = list(map(int, input().split()))
M = int(input())

block = int(N ** 0.5) + 1
queries = []
for i in range(M):
    l, r = map(int, input().split())
    queries.append((l - 1, r - 1, i))

queries.sort(key=lambda x: (x[0] // block, x[1] if (x[0] // block) % 2 == 0 else -x[1]))

result = [0] * M
freq = defaultdict(deque)
dist_count = defaultdict(int)
current_max = 0

def update_dist(v):
    dq = freq[v]
    if len(dq) >= 2:
        return dq[-1] - dq[0]
    return 0

def add(idx):
    global current_max
    v = arr[idx]
    dq = freq[v]

    old_dist = update_dist(v)
    if old_dist > 0:
        dist_count[old_dist] -= 1

    if not dq or idx > dq[-1]:
        dq.append(idx)
    else:
        dq.appendleft(idx)

    new_dist = update_dist(v)
    if new_dist > 0:
        dist_count[new_dist] += 1
        current_max = max(current_max, new_dist)

def remove(idx):
    global current_max
    v = arr[idx]
    dq = freq[v]

    old_dist = update_dist(v)
    if old_dist > 0:
        dist_count[old_dist] -= 1

    if dq[0] == idx:
        dq.popleft()
    else:
        dq.pop()

    new_dist = update_dist(v)
    if new_dist > 0:
        dist_count[new_dist] += 1

    while current_max > 0 and dist_count[current_max] == 0:
        current_max -= 1

l, r = 0, -1
for ql, qr, qi in queries:
    while l > ql:
        l -= 1
        add(l)
    while r < qr:
        r += 1
        add(r)
    while l < ql:
        remove(l)
        l += 1
    while r > qr:
        remove(r)
        r -= 1
    result[qi] = current_max

print('\n'.join(map(str, result)))
