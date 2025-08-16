import sys

input = sys.stdin.readline
N,M = map(int,input().split())
adj = {}
for i in range(1,N+1):
    favorite_nums = list(map(int,input().split()))[1:]
    adj[i] = favorite_nums

def dfs(num,visited,matched):
    if visited[num]:
        return False
    visited[num] = True
    for i in adj[num]:
        if matched[i] == -1 or dfs(matched[i],visited,matched):
            matched[i] = num
            return True
    return False

def nf():
    matched = [-1] * (M + 1)
    flow = 0
    for i in range(1,N+1):
        visited = [False] * (N+1)
        if dfs(i,visited,matched):
            flow += 1
    return flow

print(nf())