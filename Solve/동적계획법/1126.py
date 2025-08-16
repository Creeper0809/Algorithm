N = int(input())
block_height = list(map(int, input().split()))

MAXD = sum(block_height)
dp = [[-1] * (MAXD + 1) for _ in range(N)]
dp[0][block_height[0]] = 0
dp[0][0] = 0

for i in range(1, N):
    h = block_height[i]
    for d in range(MAXD):
        prev = dp[i-1][d]
        if prev == -1:
            continue
        dp[i][d] = max(dp[i][d], prev)
        if d + h <= MAXD:
            dp[i][d + h] = max(dp[i][d + h], prev)
        if h > d:
            new_d = h - d
            dp[i][new_d] = max(dp[i][new_d], prev + d)
        else:
            new_d = d-h
            dp[i][new_d] = max(dp[i][new_d], prev + h)
print(dp[N-1][0] if dp[N-1][0] > 0 else -1)