import sys
from collections import deque

EPS = 1e-9

class Dinic:

    def __init__(self, n):
        self.n = n
        self.graph = [{} for _ in range(n)]
        self.level = [-1] * n
        self.iter = [0] * n

    def add_edge(self, u, v, cap):
        self.graph[u][v] = cap
        self.graph[v][u] = 0

    def bfs(self, s):
        self.level = [-1] * self.n
        self.level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v, cap in self.graph[u].items():
                if cap > EPS and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    q.append(v)

    def dfs(self, u, t, f):
        if u == t:
            return f

        neighbors = list(self.graph[u].keys())
        while self.iter[u] < len(neighbors):
            v = neighbors[self.iter[u]]
            cap = self.graph[u][v]

            if cap > EPS and self.level[u] < self.level[v]:
                d = self.dfs(v, t, min(f, cap))
                if d > EPS:
                    self.graph[u][v] -= d
                    self.graph[v][u] += d
                    return d
            self.iter[u] += 1
        return 0

    def max_flow(self, s, t):
        flow = 0
        while True:
            self.bfs(s)
            if self.level[t] < 0:
                return flow
            self.iter = [0] * self.n
            while True:
                f = self.dfs(s, t, float('inf'))
                if f < EPS:
                    break
                flow += f

    def get_s_side_nodes(self, s):
        s_side_nodes = set()
        q = deque([s])
        s_side_nodes.add(s)
        while q:
            u = q.popleft()
            for v, cap in self.graph[u].items():
                if cap > EPS and v not in s_side_nodes:
                    s_side_nodes.add(v)
                    q.append(v)
        return s_side_nodes



input = sys.stdin.readline
N, M = map(int, input().split())
pairs = [list(map(int, input().split())) for _ in range(M)]

low = 0.0
high = float(M)

for _ in range(100):
    g = (low + high) / 2
    source = 0
    sink = 1
    num_nodes = 2 + N + M

    dinic = Dinic(num_nodes)

    total_pair_value = 0

    for i in range(M):
        u, v = pairs[i]
        pair_node_idx = N + 2 + i
        person_node_u_idx = u + 1
        person_node_v_idx = v + 1

        dinic.add_edge(source, pair_node_idx, 1.0)
        total_pair_value += 1.0

        dinic.add_edge(pair_node_idx, person_node_u_idx, float('inf'))
        dinic.add_edge(pair_node_idx, person_node_v_idx, float('inf'))

    for i in range(N):
        person_node_idx = i + 2
        dinic.add_edge(person_node_idx, sink, g)

    min_cut_val = dinic.max_flow(source, sink)

    if total_pair_value - min_cut_val > EPS:
        low = g
    else:
        high = g

if high < EPS:
    print(1)
    print(1)
    exit(0)

g = high - EPS
source = 0
sink = 1
num_nodes = 2 + N + M
dinic_final = Dinic(num_nodes)

for i in range(M):
    u, v = pairs[i]
    pair_node_idx = N + 2 + i
    person_node_u_idx = u + 1
    person_node_v_idx = v + 1
    dinic_final.add_edge(source, pair_node_idx, 1.0)
    dinic_final.add_edge(pair_node_idx, person_node_u_idx, float('inf'))
    dinic_final.add_edge(pair_node_idx, person_node_v_idx, float('inf'))

for i in range(N):
    person_node_idx = i + 2
    dinic_final.add_edge(person_node_idx, sink, g)

dinic_final.max_flow(source, sink)
final_cut_nodes = dinic_final.get_s_side_nodes(source)

team = []
for i in range(N):
    person_node_idx = i + 2
    if person_node_idx in final_cut_nodes:
        team.append(i + 1)

print(len(team))
print("\n".join(map(str, sorted(team))))