N,M = map(int,input().split())
arr = list(map(int,input().split()))
graph = [[0]*M for _ in range(N)]
for i in range(M):
    for j in range(N-1,N-arr[i]-1,-1):
        graph[j][i] = 1
answer = 0
for i in range(N):
    flag = False
    temp = 0
    for j in range(M):
        if flag:
            if graph[i][j] == 1:
                answer += temp
                temp = 0
            else:
                temp += 1
        if graph[i][j] == 1 and not flag:
            flag = True
print(answer)