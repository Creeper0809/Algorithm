N = int(input())
dp =[[0,""]] * (N+1)

for i in range(2,N+1):
    dp[i] = [dp[i - 1][0] + 1,dp[i-1][1]+" " + str(i)]
    if i % 3 == 0:
        if dp[i//3][0] + 1 < dp[i][0]:
            dp[i] = [dp[i//3][0]+1,dp[i//3][1]+" " + str(i)]
    if i % 2 == 0:
        if dp[i // 2][0] + 1 < dp[i][0]:
            dp[i] = [dp[i // 2][0] + 1, dp[i // 2][1]+" " + str(i)]
print(dp[N][0])
print(*reversed(list(map(int,dp[N][1].split()))),sep=" ",end=" ")
print(1)
