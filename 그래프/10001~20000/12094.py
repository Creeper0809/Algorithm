import sys
sys.setrecursionlimit(10**5)
N = int(input())
graph = [list(map(int, input().split())) for _ in range(N)]
answer = 0
dp = [0] * 11

def move_right(graph):
    max_val = 0
    for i in range(N):
        visited = [False] * N
        temp = [0] * N
        size = -1
        for j in range(N-1, -1, -1):
            if graph[i][j] == 0:
                continue
            if size != -1 and temp[size] == graph[i][j] and not visited[size]:
                temp[size] *= 2
                visited[size] = True
            else:
                size += 1
                temp[size] = graph[i][j]
        temp.reverse()
        graph[i] = temp
        max_val = max(max_val, max(temp))
    return max_val

def move_left(graph):
    max_val = 0
    for i in range(N):
        visited = [False] * N
        temp = [0] * N
        size = -1
        for j in range(N):
            if graph[i][j] == 0:
                continue
            if size != -1 and temp[size] == graph[i][j] and not visited[size]:
                temp[size] *= 2
                visited[size] = True
            else:
                size += 1
                temp[size] = graph[i][j]
        graph[i] = temp
        max_val = max(max_val, max(temp))
    return max_val

def move_up(graph):
    max_val = 0
    for j in range(N):
        visited = [False] * N
        temp = [0] * N
        size = -1
        for i in range(N):
            if graph[i][j] == 0:
                continue
            if size != -1 and temp[size] == graph[i][j] and not visited[size]:
                temp[size] *= 2
                visited[size] = True
            else:
                size += 1
                temp[size] = graph[i][j]
        for i in range(N):
            graph[i][j] = temp[i]
            max_val = max(max_val, temp[i])
    return max_val

def move_down(graph):
    max_val = 0
    for j in range(N):
        visited = [False] * N
        temp = [0] * N
        size = -1
        for i in range(N-1, -1, -1):
            if graph[i][j] == 0:
                continue
            if size != -1 and temp[size] == graph[i][j] and not visited[size]:
                temp[size] *= 2
                visited[size] = True
            else:
                size += 1
                temp[size] = graph[i][j]
        temp.reverse()
        for i in range(N):
            graph[i][j] = temp[i]
            max_val = max(max_val, temp[i])
    return max_val

event = [move_up, move_down, move_right, move_left]

def back_track(graph,depth,max_graph):
    global answer
    if depth == 10:
        if answer < max_graph:
            answer = max_graph
            for i in range(10, -1, -1):
                dp[i] = max_graph
                max_graph //= 2
        return


    for i in range(4):
        previous_graph = [row[:] for row in graph]
        max_after_move = event[i](previous_graph)
        if graph == previous_graph:
            continue
        if max_after_move < dp[depth + 1]:
            continue
        back_track(previous_graph,depth + 1,max_after_move)
if N == 1:
    print(graph[0][0])
    exit()
back_track(graph,0,0)
print(answer)
