import sys
from collections import deque

sys.setrecursionlimit(10**5)

dir = [[1,0],[-1,0],[0,-1],[0,1]]
R,C = map(int,input().split())
graph = [list(map(int,input())) for _ in range(R)]
visited = [[0] * C for _ in range(R)]
def bfs(start):
    queue = deque()
    queue.append(start)
    count = 1
    wall = set()
    while queue:
        r, c = queue.popleft()
        for dr, dc in dir:
            ddr = r + dr
            ddc = c + dc
            if 0 <= ddr < R and 0 <= ddc < C:
                if graph[ddr][ddc] == 0:
                    if visited[ddr][ddc] == 0:
                        visited[ddr][ddc] = 1
                        queue.append((ddr, ddc))
                        count += 1
                else:
                    wall.add((ddr,ddc))
    for r,c in wall:
        graph[r][c] += count

for i in range(R):
    for j in range(C):
        if visited[i][j] == 0 and graph[i][j] == 0:
            visited[i][j] = 1
            bfs((i,j))
for i in graph:
    for j in i:
        print(j%10,end="")
    print("")