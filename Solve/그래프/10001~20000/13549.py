from collections import deque

N,M = list(map(int,input().split()))
visited = [-1] * (100001)
queue = deque()
queue.append(N)
visited[N] = 0
while queue:
    temp = queue.popleft()
    count = visited[temp]
    if temp == M:
        print(count)
        break
    if 0<=temp-1<100001 and visited[temp-1] == -1:
        queue.append(temp-1)
        visited[temp-1] = count + 1
    if 0<=temp*2<100001 and visited[temp*2] == -1:
        queue.appendleft(temp*2)
        visited[temp*2] = count                     # 여기서 + 1 해주면 1697문제의 답
    if 0<=temp+1<100001 and visited[temp+1] == -1:
        queue.append(temp+1)
        visited[temp+1] = count + 1
