from collections import deque

N = int(input())
graph = [list(map(int,input().split())) for _ in range(N)]

dir = [[-1, 0], [0, -1], [1, 0], [0, 1]]

shark_size = 2
eat = 0
startx = 0
starty = 0
time = 0
for i in range(N):
    for j in range(N):
        if graph[i][j] == 9:
            starty = i
            startx = j

def bfs(x,y):
    global shark_size
    global time
    global starty
    global startx
    graph[y][x] = 0
    visited = [[-1]*N for _ in range(N)]
    visited[y][x] = 0
    queue = deque()
    queue.append((y,x))
    temp = []
    min_time = -1
    while queue:
        r,c = queue.popleft()
        for dr,dc in dir:
            ddr = dr+r
            ddc = dc +c
            if 0<=ddr<N and 0<=ddc<N and graph[ddr][ddc] <= shark_size and visited[ddr][ddc] == -1:
                visited[ddr][ddc] = visited[r][c] + 1
                if graph[ddr][ddc] != 0 and graph[ddr][ddc] < shark_size:
                    if min_time == -1:
                        min_time = visited[ddr][ddc]
                        temp.append((ddr,ddc))
                    if visited[ddr][ddc] == min_time:
                        temp.append((ddr,ddc))
                if min_time == -1:
                    queue.append((ddr,ddc))
    if len(temp) == 0:
        return False
    temp.sort(key=lambda x : (x[0],x[1]))
    dy, dx = temp[0]
    startx = dx
    starty = dy
    time += visited[dy][dx]
    return True

while True:
    if bfs(startx,starty):
        eat += 1
        if eat == shark_size:
            shark_size += 1
            eat = 0
    else:
        break
print(time)