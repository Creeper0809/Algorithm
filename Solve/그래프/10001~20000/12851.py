from collections import deque

N,M = list(map(int,input().split()))
visited = [[-1] * 2 for _ in range(100001)]
queue = deque()
queue.append(N)
visited[N][0] = 0
visited[N][1] = 1
while queue:
    temp = queue.popleft()
    count = visited[temp]
    if 0<=temp-1<100001 and visited[temp-1]:
        if visited[temp - 1][0] == -1:
            queue.append(temp - 1)
            visited[temp - 1][0] = visited[temp][0] + 1
            visited[temp - 1][1] = visited[temp][1]
        elif visited[temp - 1][0] == visited[temp][0] + 1:
            visited[temp - 1][1] += visited[temp][1]
    if 0<=temp*2<100001 and visited[temp*2]:
        if visited[temp * 2][0] == -1:
            queue.append(temp * 2)
            visited[temp * 2][0] = visited[temp][0] + 1
            visited[temp * 2][1] = visited[temp][1]
        elif visited[temp * 2][0] == visited[temp][0] + 1:
            visited[temp * 2][1] += visited[temp][1]
    if 0<=temp+1<100001:
        if visited[temp+1][0] == -1:
            queue.append(temp+1)
            visited[temp+1][0] = visited[temp][0] + 1
            visited[temp+1][1] = visited[temp][1]
        elif visited[temp + 1][0] == visited[temp][0] + 1:
            visited[temp + 1][1] += visited[temp][1]


print(visited[M][0])
print(visited[M][1])