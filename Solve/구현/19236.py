import copy

graph = [[0] * 4 for _ in range(4)]
direction = [[0] * 4 for _ in range(4)]
dir = [[-1, 0], [-1, -1], [0, -1], [1, -1],[1,0],[1,1],[0,1],[-1,1]]
for i in range(4):
    arr = list(map(int,input().split()))
    for j in range(0,8,2):
        graph[i][j//2] = arr[j]
        direction[i][j//2] = arr[j+1] - 1

max_score = 0
def move(n,graph,direction):
    for i in range(4):
        for j in range(4):
            if n == graph[i][j]:
                while True:
                    dy, dx = dir[direction[i][j]]
                    if 0 <= i + dy < 4 and 0 <= j + dx < 4 and graph[i + dy][j + dx] != -1:
                        temp = graph[i][j]
                        graph[i][j] = graph[i + dy][j + dx]
                        graph[i + dy][j + dx] = temp
                        temp = direction[i][j]
                        direction[i][j] = direction[i + dy][j + dx]
                        direction[i + dy][j + dx] = temp
                        return
                    direction[i][j] = (direction[i][j] + 1) % 8

def dfs(r,c,score,graph,direction):
    global max_score
    score += graph[r][c]
    graph[r][c] = -1
    for k in range(1,17):
        move(k,graph,direction)
    shark_dir = dir[direction[r][c]]
    graph[r][c] = 0
    for i in range(1,5):
        dr = r + shark_dir[0]*i
        dc = c + shark_dir[1]*i
        if 0 <= dr < 4 and 0 <= dc < 4 and graph[dr][dc] > 0:
            dfs(dr,dc,score,copy.deepcopy(graph),copy.deepcopy(direction))
    max_score = max(score, max_score)

dfs(0,0,0,graph.copy(),direction.copy())
print(max_score)