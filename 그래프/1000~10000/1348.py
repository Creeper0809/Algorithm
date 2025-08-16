from collections import deque, defaultdict

R,C = map(int,input().split())
graph = [list(input()) for _ in range(R)]
dir = [[1,0],[-1,0],[0,-1],[0,1]]
adj = defaultdict(list)


def get_id(x,y):
    return x * R + y


sink = get_id(R - 1, C - 1) + 1


def bfs(starty,startx):
    visited = [[-1]*C for _ in range(R)]
    queue = deque()

    queue.append((starty,startx))
    visited[starty][startx] = 0
    id = get_id(starty,startx)
    is_parkable = False

    while queue:
        r,c = queue.popleft()
        for dr,dc in dir:
            ddr = r + dr
            ddc = c + dc
            if 0<=ddr<R and 0<=ddc<C and graph[ddr][ddc] != "X" and visited[ddr][ddc] == -1:
                visited[ddr][ddc] = visited[r][c] + 1
                queue.append((ddr,ddc))
                if graph[ddr][ddc] == "P":
                    is_parkable = True
                    adj[id].append((visited[ddr][ddc],get_id(ddr,ddc)))
    return is_parkable


def dfs(num,limit,matched,visited):
    if visited[num]:
        return False
    visited[num] = True

    for cost,path in adj[num]:
        if cost > limit:
            continue
        if matched[path] == -1 or dfs(matched[path],limit,matched,visited):
            matched[path] = num
            return True
    return False


def nf(limit,cnt):
    matched = [-1] * sink
    flow = 0
    for i in range(R):
        for j in range(C):
            if graph[i][j] != "C":
                continue
            visited = [False] * sink
            if dfs(get_id(i,j),limit,matched,visited):
                flow += 1
    return flow == cnt


def solution():
    car_cnt = 0
    park_cnt = 0
    for i in range(R):
        for j in range(C):
            if graph[i][j] == "C":
                car_cnt += 1
                if not bfs(i,j):
                    return -1
            elif graph[i][j] == "P":
                park_cnt += 1

    if car_cnt > park_cnt:
        return -1
    if car_cnt == 0:
        return 0

    low = 0
    high = 10000000
    while low + 1 < high:
        mid = (low + high) // 2
        if nf(mid,car_cnt):
            high = mid
        else:
            low = mid
    return high

print(solution())
