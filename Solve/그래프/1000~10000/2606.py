from collections import deque

N = int(input())
M= int(input())

nodes = [[] for _ in range(N + 1)]
for _ in range(M):
    node1,node2 = list(map(int,input().split()))
    nodes[node1].append(node2)
    nodes[node2].append(node1)

def bfs(start):
    queue = deque()
    visited = [False] * (N+1)
    queue.append(start)
    visited[start] = True
    count = -1
    while queue:
        num = queue.popleft()
        count += 1
        linkedNode = nodes[num]
        for i in linkedNode:
            if not visited[i]:
                queue.append(i)
                visited[i] = True
    return count
print(bfs(1))