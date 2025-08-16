N = int(input())
graph = [list(map(int,input().split())) for _ in range(N)]

dp = [graph[0]]
dp += [[0] * 3 for _ in range(1,N)]

for i in range(1,N):
    dp[i][0] = min(dp[i-1][1],dp[i-1][2]) + graph[i][0]
    dp[i][1] = min(dp[i - 1][0], dp[i - 1][2]) + graph[i][1]
    dp[i][2] = min(dp[i - 1][1], dp[i - 1][0]) + graph[i][2]

print(min(dp[N-1]))
