from collections import deque

R,C = list(map(int,input().split()))
lake = []
swan = []
water = deque()
dir = [[1,0],[-1,0],[0,-1],[0,1]]

for i in range(R):
    tempList = list(input())
    for j in range(C):
        if tempList[j] == "." or tempList[j] == "L":
            # i가 Row j가 Colum
            water.append((j,i))
        if tempList[j] == "L":
            swan.append((i,j))
    lake.append(tempList)
# 백조 탐색 -> 녹이기 -> 백조탐색


def find_swan(queue,visited):
    nextDayDeque = deque()
    while queue:
        #y가 Row x가 colum
        (x,y) = queue.popleft()
        if y == swan[1][0] and x == swan[1][1]:
            return True,None
        for dx, dy in dir:
            ddx = x + dx
            ddy = y + dy
            if 0<=ddx<C and 0<=ddy<R and not visited[ddy][ddx]:
                if lake[ddy][ddx] == "X":
                    nextDayDeque.append((ddx,ddy))
                else:
                    queue.append((ddx,ddy))
                visited[ddy][ddx] = True
    return False,nextDayDeque


def melt_ice(water):
    nextDayWater = deque()
    while water:
        x,y = water.popleft()
        for dx,dy in dir:
            ddx = x + dx
            ddy = y + dy
            if 0 <= ddx < C and 0 <= ddy < R:
                if lake[ddy][ddx] == "X":
                    nextDayWater.append((ddx,ddy))
                    lake[ddy][ddx] = "."
    return nextDayWater


day = 0
queue = deque()
queue.append((swan[0][1],swan[0][0]))
visited = [[False] * C for _ in range(R)]
visited[swan[0][0]][swan[0][1]] = True
while True:
    found,nextDayQueue = find_swan(queue,visited)
    if found:
        break
    queue = nextDayQueue
    water = melt_ice(water)
    day += 1
print(day)