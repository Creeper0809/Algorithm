from collections import deque

N = int(input())
dir = [[1,0],[-1,0],[0,-1],[0,1]]

def bfs(graph,start,R,C):
    queue = deque()
    queue.append((start))
    visited = [[-1] * (C+2) for _ in range(R+2)]
    visited[start[0]][start[1]] = 0
    while queue:
        r,c = queue.popleft()
        for dr,dc in dir:
            ddr = r + dr
            ddc = c + dc
            if 0<=ddr<R+2 and 0<=ddc<C+2 and graph[ddr][ddc] != "*" and visited[ddr][ddc] == -1:
                if graph[ddr][ddc] == "#":
                    visited[ddr][ddc] = visited[r][c] + 1
                    queue.append((ddr,ddc))
                else:
                    visited[ddr][ddc] = visited[r][c]
                    queue.appendleft((ddr,ddc))
    return visited

for l in range(N):
    R,C = map(int, input().split())
    input_str = ''
    for _ in range(R):
        input_str += input() + '\n'
    input_str = input_str.rstrip()
    input_str = '.' * (len(input_str.split('\n')[0]) + 2) + '\n' + \
                '\n'.join(['.' + line + '.' for line in input_str.split('\n')]) + '\n' + \
                '.' * (len(input_str.split('\n')[0]) + 2)
    array = [list(row) for row in input_str.split('\n') if row]
    person = []
    for i in range(R + 2):
        for j in range(C + 2):
            if array[i][j] == "$":
                person.append([i,j])
    person1 = bfs(array,(person[0][0],person[0][1]),R,C)
    person2 = bfs(array, (person[1][0],person[1][1]),R,C)
    co_op = bfs(array, (0,0),R,C)
    result = 999999999999999
    for i in range(R + 2):
        for j in range(C + 2):
            if array[i][j] == "*":
                continue
            temp = person1[i][j] + person2[i][j] + co_op[i][j]
            if array[i][j] == "#":
                result = min(result, temp)
            if array[i][j] == "." and temp == 0:
                result = 2
    print(result - 2)