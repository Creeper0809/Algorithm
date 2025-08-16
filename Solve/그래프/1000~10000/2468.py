from collections import deque

N = int(input())
graph = list()
dir = [[1,0],[-1,0],[0,-1],[0,1]]
for i in range(N):
    graph.append(list(map(int, input().split())))
maxnum = max(map(max, graph))

def bfs(start,visited,depth):
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
            if 0<=ddr<N and 0<=ddc<N and graph[ddr][ddc] > depth and not visited[ddr][ddc]:
                visited[ddr][ddc] = True
                queue.append((ddr,ddc))


count = 0
arr =[]
for k in range(maxnum):
    visited = [[False] * N for _ in range(N)]
    alert = 0
    for i in range(N):
        for j in range(N):
            if graph[i][j] > k and not visited[i][j]:
                bfs((i, j), visited,k)
                alert +=1
    arr.append(alert)
    count = max(alert,count)
print(count)
print(arr)