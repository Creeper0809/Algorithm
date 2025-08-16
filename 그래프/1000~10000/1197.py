import sys

sys.setrecursionlimit(10 ** 5)

N, M = map(int, input().split())
graph = []
for _ in range(M):
    _from, to, weight = map(int, input().split())
    graph.append((weight,_from,to))

parent = [i for i in range(N+1)]
graph.sort()

def find(x):
    if parent[x] == x:
        return parent[x]
    y = find(parent[x])
    parent[x] = y
    return y

def union(x,y):
    root1 = find(x)
    root2 = find(y)
    if root1 < root2:
        parent[root2] = parent[root1]
    else:
        parent[root1] = parent[root2]

answer = 0
for weight,_from,to in graph:
    if find(_from) != find(to):
        answer += weight
        union(_from,to)
print(answer)