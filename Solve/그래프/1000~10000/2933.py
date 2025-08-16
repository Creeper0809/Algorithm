from collections import deque

N,M = map(int,input().split())
cave = list()
for i in range(N):
 temp = input()
 cave.append(list(temp))
dx = [0,0,-1,1]
dy = [-1,1,0,0]
isLeft = True

def breakMineral(depth):
    global isLeft
    breaked = False
    temp = cave[N - depth]
    length = 0
    if isLeft:
        for j in range(len(temp)):
            if temp[j] == "x":
                cave[N-depth][j] = "."
                length = j
                breaked = True
                break
    else:
        for j in range(len(temp)-1,-1,-1):
            if temp[j]== "x":
                cave[N-depth][j] = "."
                length = j
                breaked = True
                break
    isLeft = not isLeft
    return (N-depth,length,breaked)

def bfs(start):
    queue = deque([start])
    visited = [[False] * M for _ in range(N)]
    visited[start[0]][start[1]] = True
    isgrounded = False
    while queue:
        (x, y) = queue.popleft()
        for m in range(4):
            nowdx = x + dx[m]
            nowdy = y + dy[m]
            if 0 <= nowdx < N and 0 <= nowdy < M and not visited[nowdx][nowdy]:
                if cave[nowdx][nowdy] == "x":
                    if nowdx == N-1:
                        isgrounded = True
                    queue.append((nowdx,nowdy))
                    visited[nowdx][nowdy] = True
    return (isgrounded, visited)

def printCave():
    for k in cave:
        print(k)
    print("-"*30)

def gravityOn(visited):
    #행을 기준으로 제일 낮은 부분이 어딘지 찾기
    minXlist = [-999999] * M
    for y in range(M):
        for x in range(N - 1, -1, -1):
            if visited[x][y]:
                minXlist[y] = x
                break
    # 클러스터의 제일 밑 y값 밑에 "x"가 어디있는지 찾고 현 height와 "x"를 찾은 높이 - min_y-1중 작은 값이어야 함
    # 큰 값이 되면 넘어가는 경우가 생김
    height = 9999999
    for y, minX in enumerate(minXlist):
        if minX == -999999:
            continue
        for x in range(minX + 1, N):
            if cave[x][y] == 'x':
                height = min(height, x - minX - 1)
                break
            if x == N - 1:
                height = min(height, x - minX)
    # 위에서 찾은 height 만큼 클러스터를 내림
    for x in range(N-1, -1, -1):
        for y in range(M):
            if not visited[x][y]:
                continue
            cave[x][y] = '.'
            cave[x+height][y] = 'x'


NN = int(input())
depths = list(map(int,input().split()))
debug = 1
for i in depths:
    #막대로 미네랄 부시기
    (x,y,breaked) = breakMineral(i)
    if not breaked:
        continue
    # 부셔진 미네랄 주변 탐색
    for h in range(4):
        ddx = x + dx[h]
        ddy = y + dy[h]
        if 0 <= ddx < N and 0 <= ddy < M:
            if cave[ddx][ddy] == ".":
                continue
            # 클러스터 무더기 탐색
            (isgrounded, visited) = bfs((ddx,ddy))
            # 땅에 붙어 있는 클러스터면 중력 영향 X
            if isgrounded:
                continue
            gravityOn(visited)
            break
    debug += 1

for i in cave:
    print(*i ,sep="")