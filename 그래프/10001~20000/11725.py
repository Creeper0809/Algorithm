from collections import deque

N = int(input())
graph = [[] for i in range(N+1)]
for _ in range(N-1):
    _from , _to = map(int,input().split())
    graph[_from].append(_to)
    graph[_to].append(_from)

parent = [0] * (N+1)
visited = [False] * (N+1)
queue = deque([1])
visited[1] = True
while queue:
    num = queue.popleft()
    linked_node = graph[num]
    for node in linked_node:
        if not visited[node]:
            visited[node] = True
            parent[node] = num
            queue.append(node)
            
for i in range(2,N+1):
    print(parent[i])


