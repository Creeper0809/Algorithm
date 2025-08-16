from collections import deque

N,M = list(map(int,input().split()))
graph = list()
dir = [[1,0],[-1,0],[0,-1],[0,1]]
for i in range(N):
    graph.append(list(map(int, input().split())))


def bfs(start,visited):
    queue = deque()
    queue.append(start)
    visited[start[0]][start[1]] = True
    homecount = 0
    while queue:
        r,c = queue.popleft()
        homecount += 1
        for dr,dc in dir:
            ddr = dr + r
            ddc = dc + c
            if 0<=ddr<N and 0<=ddc<M and graph[ddr][ddc] == 1 and not visited[ddr][ddc]:
                visited[ddr][ddc] = True
                queue.append((ddr,ddc))
    return homecount

visited = [[False] * M for _ in range(N)]
count = 0
arr = [0]
for i in range(N):
    for j in range(M):
        if graph[i][j] == 1 and not visited[i][j]:
            arr.append(bfs((i,j),visited))
            count += 1

print(count)
print(max(arr))