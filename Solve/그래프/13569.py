import sys
from collections import deque

class Dinic:
    def __init__(self, n):
        self.n = n
        self.graph = [{} for _ in range(n)]
        self.level = [-1] * n
        self.iter = [0] * n

    def add_edge(self, fr, to, cap):
        if cap <= 0:
            return
        self.graph[fr][to] = cap
        if fr not in self.graph[to]:
            self.graph[to][fr] = 0

    def bfs(self, s):
        self.level = [-1] * self.n
        self.level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in self.graph[u]:
                if self.graph[u][v] > 0 and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    q.append(v)

    def dfs(self, u, t, f):
        if u == t:
            return f
        keys = list(self.graph[u].keys())
        for i in range(self.iter[u], len(keys)):
            v = keys[i]
            self.iter[u] = i + 1
            if self.level[u] < self.level[v] and self.graph[u][v] > 0:
                d = self.dfs(v, t, min(f, self.graph[u][v]))
                if d > 0:
                    self.graph[u][v] -= d
                    self.graph[v][u] += d
                    return d
        return 0

    def max_flow(self, s, t):
        flow = 0
        while True:
            self.bfs(s)
            if self.level[t] < 0:
                return flow
            self.iter = [0] * self.n
            while True:
                f = self.dfs(s, t, sys.maxsize)
                if f == 0:
                    break
                flow += f

input = sys.stdin.readline

M, N = map(int, input().split())

A_floor = [[0] * N for _ in range(M)]
A_dec = [[0] * N for _ in range(M)]
r_floor = [0] * M
r_dec = [0] * M

for i in range(M):
    line = input().strip().split()
    for k in range(N):
        val = line[k]
        if '.' in val:
            intp, decp = val.split('.')
            A_floor[i][k] = int(intp)
            A_dec[i][k] = int(decp)
        else:
            A_floor[i][k] = int(val)
            A_dec[i][k] = 0
    val = line[N]
    if '.' in val:
        intp, decp = val.split('.')
        r_floor[i] = int(intp)
        r_dec[i] = int(decp)
    else:
        r_floor[i] = int(val)
        r_dec[i] = 0

line = input().strip().split()
c_floor = [0] * N
c_dec = [0] * N
for j in range(N):
    val = line[j]
    if '.' in val:
        intp, decp = val.split('.')
        c_floor[j] = int(intp)
        c_dec[j] = int(decp)
    else:
        c_floor[j] = int(val)
        c_dec[j] = 0

r0 = 0
r_start = 1
c0 = M + 1
c_start = M + 2
num_nodes = M + 1 + N + 1
s = num_nodes
t = num_nodes + 1

dinic = Dinic(num_nodes + 2)

arc_list = []

for i in range(M):
    ri = r_start + i
    for j in range(N - 1, -1, -1):
        cj = c_start + j
        l = A_floor[i][j]
        u = l + 1 if A_dec[i][j] > 0 else l
        arc_list.append((ri, cj, l, u))

for i in range(M - 1, -1, -1):
    ri = r_start + i
    l = r_floor[i]
    u = l + 1 if r_dec[i] > 0 else l
    arc_list.append((c0, ri, l, u))

for j in range(N):
    cj = c_start + j
    l = c_floor[j]
    u = l + 1 if c_dec[j] > 0 else l
    arc_list.append((cj, r0, l, u))

sum_r_l = sum(r_floor)
sum_r_u = sum_r_l + sum(1 for dd in r_dec if dd > 0)
sum_c_l = sum(c_floor)
sum_c_u = sum_c_l + sum(1 for dd in c_dec if dd > 0)

total_l = max(sum_r_l, sum_c_l)
total_u = min(sum_r_u, sum_c_u)
arc_list.append((r0, c0, total_l, total_u))

delta = [0] * num_nodes
for u, v, l, uu in arc_list:
    delta[u] += l
    delta[v] -= l

for u, v, l, uu in arc_list:
    cap = uu - l
    if cap > 0:
        dinic.add_edge(u, v, cap)

required_flow = 0
for node in range(num_nodes):
    if delta[node] > 0:
        dinic.add_edge(node, t, delta[node])
        required_flow += delta[node]
    elif delta[node] < 0:
        dinic.add_edge(s, node, -delta[node])

dinic.max_flow(s, t)

rounded_a = [[0] * N for _ in range(M)]
for i in range(M):
    ri = r_start + i
    for j in range(N):
        cj = c_start + j
        additional = 0
        if A_dec[i][j] > 0:
            additional = dinic.graph[cj][ri]
        rounded_a[i][j] = A_floor[i][j] + additional

rounded_row = [0] * M
for i in range(M):
    ri = r_start + i
    additional = 0
    if r_dec[i] > 0:
        additional = dinic.graph[ri][c0]
    rounded_row[i] = r_floor[i] + additional

rounded_col = [0] * N
for j in range(N):
    cj = c_start + j
    additional = 0
    if c_dec[j] > 0:
        additional = dinic.graph[r0][cj]
    rounded_col[j] = c_floor[j] + additional

for i in range(M):
    print(' '.join(map(str, rounded_a[i])) + ' ' + str(rounded_row[i]))
print(' '.join(map(str, rounded_col)))