from collections import deque

N,M,V = list(map(int,input().split()))

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
    while queue:
        num = queue.popleft()
        print(num ,end=" ")
        linkedNode = nodes[num]
        linkedNode.sort()
        for i in linkedNode:
            if not visited[i]:
                queue.append(i)
                visited[i] = True


def dfs(node,visited):
    print(node,end=" ")
    linkedNode = nodes[node]
    linkedNode.sort()
    for i in linkedNode:
        if not visited[i]:
            visited[i] = True
            dfs(i,visited)

visited = [False] * (N+1)
visited[V] = True
dfs(V,visited)
print("")
bfs(V)