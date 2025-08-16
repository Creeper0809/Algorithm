import sys
from collections import deque


N,M = map(int,input().split())
graph = list()
dir = [[1,0],[-1,0],[0,-1],[0,1],[1,1],[1,-1],[-1,1],[-1,-1]]
for i in range(N):
    graph.append(list(map(int, input().split())))


def bfs(start,visited):
    queue = deque()
    queue.append(start)
    visited[start[0]][start[1]] = 1
    while queue:
        r,c = queue.popleft()
        for dr,dc in dir:
            ddr = dr + r
            ddc = dc + c
            if 0<=ddr<N and 0<=ddc<M and graph[ddr][ddc] == 1 and visited[ddr][ddc] == 0:
                visited[ddr][ddc] = 1
                queue.append((ddr,ddc))

visited = [[0] * M for _ in range(N)]
count = 0
for i in range(N):
    for j in range(M):
        if graph[i][j] == 1 and visited[i][j] == 0:
            bfs((i,j),visited)
            count += 1
print(count)