import sys

input = sys.stdin.readline
N,M = map(int,input().split())
adj = [[] for _ in range(N+1)]
group = {}
for i in range(M):
    name = input().rstrip()
    group[name] = i
for i in range(1,N+1):
    favorite_girl = input().split()[1:]
    for j in favorite_girl:
        adj[i].append(group[j])

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

total_flow = nf()
print("YES") if total_flow == N else print(f"NO\n{total_flow}")