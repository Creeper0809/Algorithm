import sys
from collections import defaultdict

input = sys.stdin.readline

class UnionFind:
    def __init__(self, n):
        self.parent = [i for i in range(n)] # 각 원소의 부모는 자기 자신
        self.rank = [1] * n # 트리의 높이 또는 랭크
        self.set_size = [1] * n # 각 집합의 크기 (option, size tracking)
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # 경로 압축
        return self.parent[x]
    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return False # 이미 같은 집합
        # 랭크를 기준으로 루트 노드를 선택
        if self.rank[x_root] < self.rank[y_root]:
            x_root, y_root = y_root, x_root
        self.parent[y_root] = x_root
        if self.rank[x_root] == self.rank[y_root]:
            self.rank[x_root] += 1
        self.set_size[x_root] += self.set_size[y_root]
        return True
    def same(self, x, y):
        return self.find(x) == self.find(y)
    def size(self, x):
        return self.set_size[self.find(x)]

n = int(input().strip())
plates = [None] * (n + 1)
total = 0
points = []

for i in range(1, n + 1):
    s, t = map(int, input().split())
    plates[i] = (s, t)
    total += s + t
    points.append((s, i))
    points.append((t, i))

points.sort()

uf = UnionFind(n + 1)

for j in range(1, len(points)):
    if points[j - 1][0] == points[j][0]:
        uf.union(points[j - 1][1], points[j][1])

groups = defaultdict(list)
for i in range(1, n + 1):
    root = uf.find(i)
    groups[root].append(i)

sum_w = 0
for root, idxs in groups.items():
    cnt = len(idxs)
    possible = set()
    for idx in idxs:
        s, t = plates[idx]
        possible.add(s)
        possible.add(t)
    loc = sorted(possible)
    sum_w += sum(loc[:cnt])

print(total - sum_w)