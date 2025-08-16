from collections import deque

N = int(input())
dir = [[-2,1],[-2,-1],[1,-2],[-1,-2],[1,2],[-1,2],[2,1],[2,-1]]


def bfs(start,end,size):
    visited = [[-1] * size for _ in range(size)]
    visited[start[0]][start[1]] = 0
    queue = deque()
    queue.append(start)
    while queue:
        r,c = queue.popleft()
        if r == end[0] and c == end[1]:
            return visited[r][c]
        for dr,dc in dir:
            ddr = dr + r
            ddc = dc + c
            if 0<=ddr<size and 0<=ddc<size and visited[ddr][ddc] == -1:
                queue.append((ddr,ddc))
                visited[ddr][ddc] = visited[r][c] + 1

for _ in range(N):
    size = int(input())
    start = list(map(int,input().split()))
    end = list(map(int,input().split()))
    num = bfs(start,end,size)
    print(num)
