import sys, math

input = sys.stdin.readline
N, C = map(int, input().split())
arr = list(map(int, input().split()))
M = int(input())

B = int(math.sqrt(N))

queries = []
for i in range(M):
    query_l, query_r = map(int, input().split())
    queries.append((query_l - 1, query_r - 1, i))

queries.sort(key=lambda x: (x[0] // B, x[1] if x[0] // B % 2 == 0 else -x[1]))

ans = [None] * M

freq = [0] * (C + 1)
head = [-1] * (N + 2)
nxt = [-1] * (C + 1)
prv = [-1] * (C + 1)
curMax = 0

def remove_from_bucket(f, v):
    p, n = prv[v], nxt[v]
    if p != -1: nxt[p] = n
    if n != -1: prv[n] = p
    if head[f] == v: head[f] = n

def add_to_bucket(f, v):
    prv[v] = -1
    nxt[v] = head[f]
    if head[f] != -1:
        prv[head[f]] = v
    head[f] = v

def add(pos):
    global curMax
    v = arr[pos]
    f = freq[v]
    if f >= 1:
        remove_from_bucket(f, v)
    f += 1
    freq[v] = f
    add_to_bucket(f, v)
    if f > curMax:
        curMax = f

def remove(pos):
    global curMax
    v = arr[pos]
    f = freq[v]
    remove_from_bucket(f, v)
    f -= 1
    freq[v] = f
    if f >= 1:
        add_to_bucket(f, v)
    if head[curMax] == -1:
        curMax -= 1

l, r = 0, -1

for query_l, query_r, idx in queries:
    while l > query_l:
        l -= 1
        add(l)
    while r < query_r:
        r += 1
        add(r)
    while l < query_l:
        remove(l)
        l += 1
    while r > query_r:
        remove(r)
        r -= 1

    length = query_r - query_l + 1
    if curMax * 2 > length:
        ans[idx] = f"yes {head[curMax]}"
    else:
        ans[idx] = "no"

print("\n".join(ans))
