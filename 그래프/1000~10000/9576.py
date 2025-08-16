import sys
from collections import defaultdict

input = sys.stdin.readline
K = int(input())

def dfs(num,visited,matched,adj):
    if visited[num]:
        return False
    visited[num] = True
    for i in adj[num]:
        if matched[i] == -1 or dfs(matched[i],visited,matched,adj):
            matched[i] = num
            return True
    return False

def nf(N,M,adj):
    matched = [-1] * (N+1)
    flow = 0
    for i in range(1,M+1):
        visited = [False] * (M+1)
        if dfs(i,visited,matched,adj):
            flow += 1
    return flow

for _ in range(K):
    M,N = map(int, input().rstrip().split())
    adj = [[] for _ in range(N+1)]
    for i in range(1, N + 1):
        a,b = map(int, input().split())
        for j in range(a,b+1):
            adj[i].append(j)
    print(nf(M,N,adj))