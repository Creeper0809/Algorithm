import sys

sys.setrecursionlimit(10 ** 7)
input = sys.stdin.readline

N = int(input())
sharks = [tuple(map(int, input().split())) for _ in range(N)]


L = 2 * N
graph = [[] for _ in range(L)]
for i in range(N):
    for j in range(N):
        if i == j:
            continue
        ai, bi, ci = sharks[i]
        aj, bj, cj = sharks[j]
        if ai >= aj and bi >= bj and ci >= cj:
            if sharks[i] == sharks[j] and i > j:
                continue
            graph[i].append(j)
            graph[i + N].append(j)

parent = [-1] * N


def dfs(u, visited):
    for v in graph[u]:
        if not visited[v]:
            visited[v] = True
            if parent[v] == -1 or dfs(parent[v], visited):
                parent[v] = u
                return True
    return False


flow = 0
for u in range(L):
    visited = [False] * N
    if dfs(u, visited):
        flow += 1

print(N - flow)
