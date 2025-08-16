from collections import deque

N,M = map(int,input().split())
indegree = [0] * (N+1)
adj = [[] for _ in range(N+1)]
for _ in range(M):
    line_up = list(map(int,input().split()))
    for i in range(1,line_up[0]):
        for b in line_up[i+1:]:
            adj[line_up[i]].append(b)
            indegree[b] += 1

queue = deque()
for i in range(1,N+1):
    if indegree[i] == 0:
        queue.append(i)
answer = []
while queue:
    num = queue.popleft()
    answer.append(num)
    for next in adj[num]:
        indegree[next] -= 1
        if indegree[next] == 0:
            queue.append(next)
if sum(indegree) > 0:
    print(0)
else:
    [print(i) for i in answer]