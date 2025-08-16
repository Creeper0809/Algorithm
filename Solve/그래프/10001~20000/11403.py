N = int(input())
graph = [list(map(int,input().split())) for _ in range(N)]


answer = [[0] * N for _ in range(N)]


for k in range(N):                                          # 0~N까지 한개씩 집음
    for i in range(N):                                      # 0~N노드중 k노드로 연결된걸 찾음
        for j in range(N):                                  # K노드에서 0~N노드중 연결된걸 찾음
            if graph[i][k] != 0 and graph[k][j] != 0:       # 만약 i 노드와 k가 연결 돼 있고 k노드와 j노드가 연결 돼 있다면
                graph[i][j] = 1                             # i노드와 j 노드도 연결 된 것

for i in graph:
    for j in i:
        print(j ,end=" ")
    print("")