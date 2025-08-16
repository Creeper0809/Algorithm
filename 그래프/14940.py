from collections import deque

N,M = map(int,input().split())
graph = [list(map(int,input().split())) for _ in range(N)]
dir = [(0,1),(0,-1),(-1,0),(1,0)]


queue = deque()
visited = [[-1] * M for _ in range(N)]

for i in range(N):
    for j in range(M):
        if graph[i][j] == 2:
            queue.append((i, j))
            visited[i][j] = 0
        if graph[i][j] == 0:
            visited[i][j] = 0

while queue:
    x,y = queue.popleft()
    for dx,dy in dir:
        ddx = dx + x
        ddy = dy + y
        if 0 <= ddx < N and 0 <= ddy < M and graph[ddx][ddy] == 1 and visited[ddx][ddy] == -1:
            visited[ddx][ddy] = visited[x][y] + 1
            queue.append((ddx, ddy))

for i in visited:
    print(*i)


