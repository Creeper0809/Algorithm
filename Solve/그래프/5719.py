import sys
import heapq
from collections import deque, defaultdict

input = sys.stdin.readline
INF = int(1e9)

def dijkstra(start, graph, banned):
    distance = [INF] * len(graph)
    q = [(0, start)]
    distance[start] = 0
    parent = [[] for _ in range(len(graph))]

    while q:
        dist, cur = heapq.heappop(q)
        if distance[cur] < dist:
            continue
        for nxt, cost in graph[cur]:
            if (cur, nxt) in banned:
                continue
            new_cost = dist + cost
            if distance[nxt] > new_cost:
                distance[nxt] = new_cost
                parent[nxt] = [cur]
                heapq.heappush(q, (new_cost, nxt))
            elif distance[nxt] == new_cost:
                parent[nxt].append(cur)
    return distance, parent

def find_banned_edges(end, start, parent):
    banned = set()
    dq = deque()
    dq.append(end)
    visited = [False] * len(parent)
    while dq:
        cur = dq.popleft()
        for prev in parent[cur]:
            if (prev, cur) not in banned:
                banned.add((prev, cur))
                dq.append(prev)
    return banned

while True:
    N, M = map(int, input().split())
    if N == 0 and M == 0:
        break
    start, end = map(int, input().split())
    graph = [[] for _ in range(N)]
    for _ in range(M):
        u, v, p = map(int, input().split())
        graph[u].append((v, p))

    distance, parent = dijkstra(start, graph, banned=set())
    banned_edges = find_banned_edges(end, start, parent)
    distance2, _ = dijkstra(start, graph, banned_edges)
    print(distance2[end] if distance2[end] != INF else -1)
