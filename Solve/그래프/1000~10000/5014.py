from collections import deque

F, S, G, U, D = list(map(int,input().split()))
dir = [U,-D]

def bfs(start,end):
    visited = [False] * (F + 2)
    visited[start] = True
    queue = deque()
    queue.append((start,0))
    while queue:
        num,count = queue.popleft()
        if num == end:
            return count
        for dr in dir:
            ddr = dr + num
            if 1<=ddr<=F and not visited[ddr]:
                queue.append((ddr,count + 1))
                visited[ddr] = True
    return "use the stairs"

print(bfs(S,G))