import sys
import heapq

sys.setrecursionlimit(10**6)
input = sys.stdin.readline

class UnionFind:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [1] * n
        self.set_size = [1] * n
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return False
        if self.rank[x_root] < self.rank[y_root]:
            x_root, y_root = y_root, x_root
        self.parent[y_root] = x_root
        if self.rank[x_root] == self.rank[y_root]:
            self.rank[x_root] += 1
        self.set_size[x_root] += self.set_size[y_root]
        return True

N, M, K, Q = map(int, input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a, b, c = map(int, input().split())
    a -= 1
    b -= 1
    graph[a].append((b, c))
    graph[b].append((a, c))

fest = set()
for _ in range(K):
    f = int(input()) - 1
    fest.add(f)

dist_to_fest = [float('inf')] * N
hq = []
for f in fest:
    dist_to_fest[f] = 0
    heapq.heappush(hq, (0, f))

while hq:
    d, u = heapq.heappop(hq)
    if d > dist_to_fest[u]:
        continue
    for v, w in graph[u]:
        nd = d + w
        if nd < dist_to_fest[v]:
            dist_to_fest[v] = nd
            heapq.heappush(hq, (nd, v))

edges = []
for u in range(N):
    for v, _ in graph[u]:
        if u < v:
            bott = min(dist_to_fest[u], dist_to_fest[v])
            edges.append((bott, u, v))

edges.sort(reverse=True)

uf = UnionFind(N)
tree = [[] for _ in range(N)]
for bott, u, v in edges:
    if uf.union(u, v):
        tree[u].append((v, bott))
        tree[v].append((u, bott))

LOG = 18
parent = [[-1] * N for _ in range(LOG)]
min_edge = [[float('inf')] * N for _ in range(LOG)]
depth = [0] * N
vis = [False] * N

def dfs(u, p, dep, edge_from_p):
    vis[u] = True
    parent[0][u] = p
    min_edge[0][u] = edge_from_p
    depth[u] = dep
    for v, bott in tree[u]:
        if not vis[v]:
            dfs(v, u, dep + 1, bott)

dfs(0, -1, 0, float('inf'))

for k in range(1, LOG):
    for i in range(N):
        if parent[k-1][i] != -1:
            parent[k][i] = parent[k-1][parent[k-1][i]]
            min_edge[k][i] = min(min_edge[k-1][i], min_edge[k-1][parent[k-1][i]])

def get_min_on_path(u, v):
    min_path = float('inf')
    if depth[u] > depth[v]:
        u, v = v, u
    diff = depth[v] - depth[u]
    k = 0
    while diff:
        if diff & 1:
            min_path = min(min_path, min_edge[k][v])
            v = parent[k][v]
        diff >>= 1
        k += 1
    if u == v:
        return min_path
    for k in range(LOG - 1, -1, -1):
        if parent[k][u] != parent[k][v]:
            min_path = min(min_path, min_edge[k][u], min_edge[k][v])
            u = parent[k][u]
            v = parent[k][v]
    min_path = min(min_path, min_edge[0][u], min_edge[0][v])
    return min_path

for _ in range(Q):
    s, t = map(int, input().split())
    s -= 1
    t -= 1
    ans = get_min_on_path(s, t)
    print(ans)