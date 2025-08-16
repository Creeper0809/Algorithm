N,K = map(int,input().split())
items =[] + [list(map(int,input().split())) for _ in range(N)]

dp = [[0] * (K + 1) for _ in range(N)]

for i in range(N):
    for j in range(K+1):
        weight,cost = items[i]
        if weight <= j:
            dp[i][j] = max(dp[i-1][j],dp[i-1][j-weight] + cost)
        else:
            dp[i][j] = dp[i-1][j]

print(dp[N-1][K])