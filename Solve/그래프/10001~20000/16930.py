from collections import deque

N,M, K = map(int, input().split())
graph = list()
dir = [[1,0],[-1,0],[0,-1],[0,1]]
for i in range(N):
    graph.append(list(input()))

x1,y1,x2,y2 = map(int,input().split())


def bfs(x1,y1,x2,y2,visited):
    queue = deque()
    queue.append((x1,y1))
    visited[x1][y1] = 0
    while queue:
        x,y = queue.popleft()
        for i in range(4):
            for j in range(1, K + 1):
                ddx = x + (dir[i][0] * j)
                ddy = y + (dir[i][1] * j)
                if 0 <= ddx < N and 0 <= ddy < M and graph[ddx][ddy] == ".":
                    if visited[ddx][ddy] == -1:
                        if ddx == x2 and ddy == y2:
                            return visited[x][y] + 1
                        queue.append((ddx, ddy))
                        visited[ddx][ddy] = visited[x][y] + 1
                    elif visited[ddx][ddy] <= visited[x][y]:
                        break
                else:
                    break
    return -1

visited = [[-1] * M for _ in range(N)]
x1 -= 1
y1 -= 1
x2 -= 1
y2 -= 1
print(bfs(x1,y1,x2,y2,visited))
