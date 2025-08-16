import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline

n, m = map(int, input().split())
in_list = [0] * (n + 1)
out_list = [0] * (n + 1)
timer = 0
graph = [[] for _ in range(n + 1)]
adj = list(map(int, input().split()))
visited = [False] * (n + 1)

for i in range(n):
    to = adj[i]
    if to == -1:
        continue
    graph[i + 1].append(to)
    graph[to].append(i + 1)

def dfs(idx):
    global timer
    if visited[idx]:
        return
    visited[idx] = True
    timer += 1
    in_list[idx] = timer
    for i in graph[idx]:
        dfs(i)
    out_list[idx] = timer

dfs(1)

seg_tree = [0] * (4 * (n + 1))
lazy = [0] * (4 * (n + 1))

def update_lazy(node, start, end):
    if lazy[node] != 0:
        seg_tree[node] += (end - start + 1) * lazy[node]
        if start != end:
            lazy[2 * node] += lazy[node]
            lazy[2 * node + 1] += lazy[node]
        lazy[node] = 0

def query(left, right, node=1, start=0, end=n):
    update_lazy(node, start, end)
    if left > end or right < start:
        return 0
    if left <= start and right >= end:
        return seg_tree[node]
    mid = (start + end) // 2
    return query(left, right, node * 2, start, mid) + query(left, right, node * 2 + 1, mid + 1, end)

def update_range(left, right, val, node=1, start=0, end=n):
    update_lazy(node, start, end)
    if left > end or right < start:
        return
    if left <= start and end <= right:
        seg_tree[node] += (end - start + 1) * val
        if start != end:
            lazy[2 * node] += val
            lazy[2 * node + 1] += val
        return
    mid = (start + end) // 2
    update_range(left, right, val, 2 * node, start, mid)
    update_range(left, right, val, 2 * node + 1, mid + 1, end)
    seg_tree[node] = seg_tree[2 * node] + seg_tree[2 * node + 1]

for _ in range(m):
    query_string = list(map(int, input().split()))
    if query_string[0] == 1:
        update_range(in_list[query_string[1]], out_list[query_string[1]], query_string[2])
    else:
        print(query(in_list[query_string[1]], in_list[query_string[1]]))
