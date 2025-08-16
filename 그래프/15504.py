from collections import deque
import sys

class Edge:
    def __init__(self, to, cap, cost):
        self.to = to
        self.cap = cap
        self.cost = cost
        self.flow = 0
        self.rev = None

def add_edge(graph, fr, to, cap, cost):
    forward = Edge(to, cap, cost)
    backward = Edge(fr, 0, -cost)
    forward.rev = backward
    backward.rev = forward
    graph[fr].append(forward)
    graph[to].append(backward)

def spfa(graph, s, t, dist, parent):
    n = len(graph)
    in_queue = [False] * n
    dist[:] = [float('inf')] * n
    dist[s] = 0
    queue = deque([s])
    while queue:
        u = queue.popleft()
        in_queue[u] = False
        for e in graph[u]:
            if e.cap - e.flow > 0 and dist[e.to] > dist[u] + e.cost:
                dist[e.to] = dist[u] + e.cost
                parent[e.to] = (u, e)
                if not in_queue[e.to]:
                    in_queue[e.to] = True
                    queue.append(e.to)
    return dist[t] != float('inf')

def min_cost_max_flow(graph, s, t):
    flow = 0
    cost = 0
    n = len(graph)
    dist = [0] * n
    parent = [None] * n
    while spfa(graph, s, t, dist, parent):
        path_flow = float('inf')
        v = t
        while v != s:
            u, e = parent[v]
            path_flow = min(path_flow, e.cap - e.flow)
            v = u
        v = t
        while v != s:
            u, e = parent[v]
            e.flow += path_flow
            e.rev.flow -= path_flow
            cost += path_flow * e.cost
            v = u
        flow += path_flow
    return flow, cost

input = sys.stdin.readline
N = int(input())
A = [0] + list(map(int, input().split()))
H = [0] + list(map(int, input().split()))
L = [0] + list(map(int, input().split()))

winner = 1
for i in range(2, N + 1):
    if A[i] > A[winner]:
        winner = i

source = 0
sink = 2 * N + 1
graph = [[] for _ in range(2 * N + 2)]

for i in range(1, N + 1):
    if i != winner:
        add_edge(graph, source, i, 1, 0)

for i in range(1, N + 1):
    for j in range(1, N + 1):
        if i != j and A[i] < A[j]:
            add_edge(graph, i, N + j, 1, H[i] + H[j] - (A[i] ^ A[j]))

for i in range(1, N + 1):
    cap = L[i] if i == winner else L[i] - 1
    add_edge(graph, N + i, sink, cap, 0)

flow, cost = min_cost_max_flow(graph, source, sink)
print(-cost)