from collections import deque

N = int(input())
arr = [list(map(int,input().split())) for _ in range(N)]
dir = [[0,1],[1,0]]
def bfs(start):
    visited = [[False] * N for _ in range(N)]
    queue = deque([start])
    while queue:
        (y,x) = queue.popleft()
        temp = arr[y][x]
        if temp == -1:
            return "HaruHaru"
        for dx,dy in dir:
            if 0 <= x + dx * temp < N and 0 <= y + dy * temp < N and not visited[y + dy * temp][x + dx * temp]:
                queue.append((y + dy * temp,x + dx * temp))
                visited[y + dy * temp][x + dx * temp] = True
    return "Hing"
print(bfs((0,0)))