from collections import deque

dir = [[1, 0], [-1, 0], [0, -1], [0, 1]]
N = int(input())

key = {}
for i in range(97,123):
    key[chr(i)] = i-97

def bfs(x,y,key_holding,graph):
    queue = deque()
    visited = [[False] * (C+2) for _ in range(R+2)]
    queue.append((x,y))
    visited[x][y] = True
    count = 0
    while queue:
        r,c = queue.popleft()
        for dr,dc in dir:
            ddr = dr + r
            ddc = dc + c
            if 0<=ddr<R+2 and 0<=ddc<C+2 and graph[ddr][ddc] != "*" and not visited[ddr][ddc]:
                space = graph[ddr][ddc]
                if "a"<=space<="z":
                    key_holding |= (1<<key[space])
                    visited = [[False] * (C+2) for _ in range(R+2)]
                    visited[ddr][ddc] = True
                    graph[ddr][ddc] = "."
                    queue = deque()
                    queue.append((ddr,ddc))
                elif "A"<=space<="Z" and key_holding & (1 << key[space.lower()]):
                    visited[ddr][ddc] = True
                    graph[ddr][ddc] = "."
                    queue.append((ddr,ddc))
                elif space == ".":
                    visited[ddr][ddc]= True
                    queue.append((ddr, ddc))
                elif space == "$":
                    visited[ddr][ddc] = True
                    graph[ddr][ddc] = "."
                    queue.append((ddr, ddc))
                    count += 1
    return count
for _ in range(N):
    R, C = map(int, input().split())
    temp = [list(input()) for _ in range(R)]
    graph = [["."] * (C+2)]
    for i in temp:
        graph.append(["."] + i + ["."])
    graph.append(["."] * (C+2))
    haskeylist = input()
    keyholding = 0
    for i in haskeylist:
        if i == '0':
            break
        keyholding |= (1<<key[i])
    print(bfs(0,0,keyholding,graph))
