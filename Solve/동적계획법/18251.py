import sys
import math

sys.setrecursionlimit(10 ** 5)
input = sys.stdin.readline

N = int(input().strip())
weight = list(map(int, input().split()))
nodes = []
length = int(math.log2(N)) + 1
def DFS(idx, x, y):
    if idx * 2 <= N:
        x = DFS(idx * 2, x, y + 1)
    nodes.append([x, y, weight[idx - 1]])
    if idx * 2 + 1 <= N:
        x = DFS(idx * 2 + 1, x + 1, y + 1)
    return x + 1
DFS(1,0,0)
ans = nodes[0][2]
for i in range(length):
    for j in range(i, length):
        s = 0
        for n in nodes:
            if n[1] < i or j < n[1]:
                continue
            if s + n[2] < 0:
                ans = max(ans, n[2])
                s = 0
            else:
                s += n[2]
                ans = max(ans, s)
print(ans)
