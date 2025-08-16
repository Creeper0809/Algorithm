N = int(input())

has_line = [[0]*101 for _ in range(101)]
dp = [[0]*101 for _ in range(101)]

for _ in range(N):
    a, b = map(int, input().split())
    has_line[a][b] = 1
    has_line[b][a] = 1
    dp[a][b] = 1

# dp[i][j] = max(dp[i][j] < 선택 X, dp[i][k] + dp[k][j] + has_line[i][j] )
for L in range(2, 100):
    for i in range(1, 101-L):
        j = i + L
        for k in range(i, j):
            dp[i][j] = max(dp[i][j], dp[i][k] + dp[k + 1][j] + has_line[k][j])

print(dp[1][100])
