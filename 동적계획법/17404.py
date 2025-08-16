N = int(input())
graph = [list(map(int,input().split())) for _ in range(N)]

answer = 1e10
for k in range(3):
    dp = [[1e10] * 3 for _ in range(N)]
    dp[0][k] = graph[0][k]
    for i in range(1,N):
        dp[i][0] = min(dp[i-1][1],dp[i-1][2]) + graph[i][0]
        dp[i][1] = min(dp[i - 1][0], dp[i - 1][2]) + graph[i][1]
        dp[i][2] = min(dp[i - 1][1], dp[i - 1][0]) + graph[i][2]
    for j in range(3):
        if k != j:
            answer = min(dp[N-1][j], answer)

print(answer)
