from collections import deque

N,M = list(map(int,input().split()))
if N == M:
    print(0)
    exit(0)
visited = [[-1] * (500001) for _ in range(2)]
queue = deque()
queue.append((N,0))
while queue:
    temp,count = queue.popleft()
    odd = count%2
    if 0<=temp-1<500001 and visited[1-odd][temp-1] == -1:
        queue.append((temp-1,count + 1))
        visited[1-odd][temp-1] = count + 1
    if 0<=temp*2<500001 and visited[1-odd][temp*2] == -1:
        queue.append((temp*2,count + 1))
        visited[1-odd][temp*2] = count + 1
    if 0<=temp+1<500001 and visited[1-odd][temp+1] == -1:
        queue.append((temp+1,count + 1))
        visited[1-odd][temp+1] = count + 1


brotherdistance = M
time = 0
res = -1
while brotherdistance < 500001:
    if visited[time%2][brotherdistance] != -1 and visited[time%2][brotherdistance]<=time:
        res = time
        break
    time += 1
    brotherdistance += time
print(res)