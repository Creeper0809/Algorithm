import sys
from collections import deque

def hopcroft_karp(graph, nL, nR):
    INF = 10**9
    pairU = [-1] * nL
    pairV = [-1] * nR
    dist = [0] * nL

    def bfs():
        q = deque()
        for u in range(nL):
            if pairU[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF
        found = False
        while q:
            u = q.popleft()
            for v in graph[u]:
                pu = pairV[v]
                if pu == -1:
                    found = True
                elif dist[pu] == INF:
                    dist[pu] = dist[u] + 1
                    q.append(pu)
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
T = int(input())
for _ in range(T):
    n, m = map(int, input().split())
    # left: u_out = [0..n-1], right: v_in = [0..n-1]
    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        # (u -> v) 간선을 u_out → v_in 으로 추가
        graph[u].append(v)
    # 최대 매칭 크기가 곧 답이다
    print(hopcroft_karp(graph, n, n))
