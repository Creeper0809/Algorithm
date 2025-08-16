from collections import deque
R,C = 12,6
graph = list()
dir = [[1,0],[-1,0],[0,-1],[0,1]]
for i in range(R):
    graph.append(list(input()))


def printPan():
    for i in graph:
        print(i)
    print("-"*30)

def bfs(start,visited):
    queue = deque()
    queue.append((start[0],start[1]))
    visited[start[0]][start[1]] = True
    group = list()
    group.append(start)
    while queue:
        r,c = queue.popleft()
        for dr,dc in dir:
            ddr = r + dr
            ddc = c + dc
            #영역 안,방문하지 않았고 이 전 알파벳과 같으면 한 영역임
            if 0<=ddr<R and 0<=ddc<C and not visited[ddr][ddc] and graph[r][c] == graph[ddr][ddc]:
                visited[ddr][ddc] = True
                queue.append((ddr,ddc))
                group.append((ddr,ddc))
    #만약 그룹에 들은게 3개 이상이라면 잠재적 부셔질 뿌요임
    if len(group) > 3:
        return group
    return []

def breakPuyo(groups):
    # 뿌요를 부시고 부신 행을 저장
    for r,c in groups:
        graph[r][c] = "."
    for i in range(C):
        howmuch = 0
        # 위에서부터 뿌요를 내리면 겹치는 상황 발생 할 수도 있으니까 아래서부터 뿌요를 내리기
        for j in range(R-1,-1,-1):
            if graph[j][i] != ".":
                # 뿌요를 발견했다면 그 밑으로 내려야 하는 만큼을 계산
                for k in range(j+1,R):
                    if graph[k][i] == ".":
                        howmuch += 1
                # 한칸이라도 내려야 한다면 내려주기
                if howmuch > 0:
                    graph[j+howmuch][i] = graph[j][i]
                    graph[j][i] = "."
                    howmuch = 0
    #printPan()
chain = 0
def checkPna():
    global chain
    groups = list()
    visited = [[False] * C for _ in range(R)]
    # 완전 탐색으로 영역 확인
    for i in range(R):
        for j in range(C):
            if graph[i][j] != "." and not visited[i][j]:
                # 4개 이상 붙어 있는 뿌요는 잠재적 부실 대상자
                groups += bfs((i, j),visited)
    return groups



#printPan()
while True:
    breaked = checkPna()
    # 부셔질 뿌요가 없다면 그만
    if len(breaked) == 0:
        break
    # 부셔질 뿌요가 있다면 부시기
    breakPuyo(breaked)
    chain += 1
print(chain)