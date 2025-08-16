from collections import deque
dir = [[1, 0], [-1, 0], [0, -1], [0, 1]]
R,C = map(int,input().split())
graph = []
redstartr = 0
redstartc = 0
bluestartr = 0
bluestartc = 0
for i in range(R):
    temp = list(input())
    if "R" in temp:
        redstartr = i
        redstartc = temp.index("R")
    if "B" in temp:
        bluestartr = i
        bluestartc = temp.index("B")
    graph.append(temp)

def move(sr,sc,d):
    dr,dc = d
    c = 0
    while graph[sr+dr][sc+dc] != "#" and graph[sr][sc] != "O":
        sr += dr
        sc += dc
        c += 1
    return sr,sc,c

def bfs():
    visited = [[[[False] * C for _ in range(R)] for _ in range(C)] for _ in range(R)]
    queue = deque()
    queue.append((redstartr,redstartc,bluestartr,bluestartc,1))
    visited[redstartr][redstartc][bluestartr][bluestartc] = True
    while queue:
        redr,redc,bluer,bluec,count = queue.popleft()
        if count > 10:
            return 0
        for i in range(4):
            reddr,reddc,redcnt = move(redr,redc,dir[i])
            bluedr,bluedc,bluecnt = move(bluer,bluec,dir[i])
            if graph[bluedr][bluedc] != "O":
                if graph[reddr][reddc] == "O":
                    return 1
                if bluedr == reddr and bluedc == reddc:
                    if redcnt < bluecnt:
                        bluedr -= dir[i][0]
                        bluedc -= dir[i][1]
                    else:
                        reddr -= dir[i][0]
                        reddc -= dir[i][1]
                if not visited[reddr][reddc][bluedr][bluedc]:
                    queue.append((reddr,reddc,bluedr,bluedc,count + 1))
                    visited[reddr][reddc][bluedr][bluedc] = True
    return 0
print(bfs())