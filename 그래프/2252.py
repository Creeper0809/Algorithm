from collections import deque

N,M = map(int,input().split())
indegree = [0] * (N+1)
adj = [[] for _ in range(N+1)]
for _ in range(M):
    _from, _to = map(int,input().split())
    adj[_from].append(_to)
    indegree[_to] += 1

queue = deque()
for i in range(1,N+1):
    if indegree[i] == 0:
        queue.append(i)

while queue:
    num = queue.popleft()
    print(num,end=" ")
    for next in adj[num]:
        indegree[next] -= 1
        if indegree[next] == 0:
            queue.append(next)