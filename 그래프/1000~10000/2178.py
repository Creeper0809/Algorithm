from collections import deque

N, M = list(map(int,input().split()))
miro = list()
dir = [[0,1],
       [1,0],
       [-1,0],
       [0,-1]]
for i in range(N):
 temp = input()
 miro.append(list(temp))

def bfs(start):
    visited = [[0] * M for _ in range(N)]
    queue = deque([start])
    visited[start[0]][start[0]] = 1
    while queue:
        (x,y) = queue.popleft()
        count = visited[x][y]
        for dx,dy in dir:
            ddx = dx + x
            ddy = dy + y
            if 0<=ddx<N and 0 <= ddy<M and int(miro[ddx][ddy]) == 1 and visited[ddx][ddy] == 0:
                if ddx == N-1 and ddy == M-1:
                    return count + 1
                queue.append((ddx,ddy))
                visited[ddx][ddy] = count + 1
print(bfs((0,0)))