from collections import deque
import sys

input = sys.stdin.readline
INF = int(1e9)

class Edge:
    def __init__(self, to, cap):
        self.to = to
        self.cap = cap
        self.flow = 0
        self.rev = None

    def residual(self):
        return self.cap - self.flow

    def push(self, amount):
        self.flow += amount
        self.rev.flow -= amount

def add_edge(graph, u, v, cap):
    fwd = Edge(v, cap)
    bwd = Edge(u, 0)
    fwd.rev = bwd
    bwd.rev = fwd
    graph[u].append(fwd)
    graph[v].append(bwd)

def bfs(graph, src, snk, parent, path_edge):
    visited = [False] * len(graph)
    queue = deque([src])
    visited[src] = True

    while queue:
        u = queue.popleft()
        for e in graph[u]:
            if not visited[e.to] and e.residual() > 0:
                visited[e.to] = True
                parent[e.to] = u
                path_edge[e.to] = e
                if e.to == snk:
                    return True
                queue.append(e.to)
    return False

def max_flow(graph, src, snk):
    total_flow = 0
    parent = [-1] * len(graph)
    path_edge = [None] * len(graph)

    while bfs(graph, src, snk, parent, path_edge):
        flow = INF
        v = snk
        while v != src:
            flow = min(flow, path_edge[v].residual())
            v = parent[v]
        v = snk
        while v != src:
            path_edge[v].push(flow)
            v = parent[v]
        total_flow += flow
    return total_flow

def reachable_from_source(graph, src):
    visited = [False] * len(graph)
    queue = deque([src])
    visited[src] = True
    while queue:
        u = queue.popleft()
        for e in graph[u]:
            if e.residual() > 0 and not visited[e.to]:
                visited[e.to] = True
                queue.append(e.to)
    return visited

n, m = map(int, input().split())
s, t = map(int, input().split())
s -= 1
t -= 1

cost = [int(input()) for _ in range(n)]
roads = [tuple(map(int, input().split())) for _ in range(m)]

SIZE = 2 * n
graph = [[] for _ in range(SIZE)]

for i in range(n):
    u_in = i * 2
    u_out = i * 2 + 1
    add_edge(graph, u_in, u_out, cost[i])

for u, v in roads:
    u -= 1
    v -= 1
    add_edge(graph, u * 2 + 1, v * 2, INF)
    add_edge(graph, v * 2 + 1, u * 2, INF)

source = s * 2 + 1
sink = t * 2

max_flow(graph, source, sink)
visited = reachable_from_source(graph, source)

answer = []
for i in range(n):
    v_in = i * 2
    v_out = i * 2 + 1
    if visited[v_in] and not visited[v_out]:
        answer.append(i + 1)

print(*sorted(answer))
