import sys

sys.setrecursionlimit(10**5)
N,M = map(int,input().split())
parent = [i for i in range(N+1)]

def find(x):
    if parent[x] == x:
        return parent[x]
    y = find(parent[x])
    parent[x] = y
    return y

def union(x,y):
    root1 = find(x)
    root2 = find(y)

    if root1<root2:
        parent[root2] = root1
    else:
        parent[root1] = root2

for _ in range(M):
    command,A,B = map(int,input().split())
    if command:
        print("YES") if find(A) == find(B) else print("NO")
    else:
        union(A,B)