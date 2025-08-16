import sys
from collections import deque

def hopcroft_karp(graph, nL, nR):
    INF = 10**9
    pairU = [-1] * nL
    pairV = [-1] * nR
    dist = [0] * nL

    def bfs():
        queue = deque()
        for u in range(nL):
            if pairU[u] == -1:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = INF
        found = False
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                pu = pairV[v]
                if pu == -1:
                    found = True
                elif dist[pu] == INF:
                    dist[pu] = dist[u] + 1
                    queue.append(pu)
        return found

    def dfs(u):
        for v in graph[u]:
            pu = pairV[v]
            if pu == -1 or (dist[pu] == dist[u] + 1 and dfs(pu)):
                pairU[u] = v
                pairV[v] = u
                return True
        dist[u] = INF
        return False

    matching = 0
    while bfs():
        for u in range(nL):
            if pairU[u] == -1 and dfs(u):
                matching += 1
    return matching

input = sys.stdin.readline
TC = int(input())
for _ in range(TC):
    c, d, v = map(int, input().split())
    L, R = [], []
    for _ in range(v):
        a, b = input().split()
        if a[0] == 'C':
            L.append((int(a[1:]), int(b[1:])))  # (cat_keep, dog_drop)
        else:
            R.append((int(a[1:]), int(b[1:])))  # (dog_keep, cat_drop)

    nL, nR = len(L), len(R)
    graph = [[] for _ in range(nL)]
    for i in range(nL):
        cat_keep, dog_drop = L[i]
        for j in range(nR):
            dog_keep, cat_drop = R[j]
            if cat_keep == cat_drop or dog_drop == dog_keep:
                graph[i].append(j)

    matching = hopcroft_karp(graph, nL, nR)
    print(v - matching)
