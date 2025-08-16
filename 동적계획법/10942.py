import sys
input = sys.stdin.readline

N = int(input())
arr = list(map(int, input().split()))
dp = [[0] * N for _ in range(N)]


for i in range(N):
    dp[i][i] = 1


for i in range(N - 1):
    if arr[i] == arr[i + 1]:
        dp[i][i + 1] = 1


for length in range(3, N + 1):
    for start in range(N - length + 1):
        end = start + length - 1
        if arr[start] == arr[end] and dp[start + 1][end - 1]:
            dp[start][end] = 1


M = int(input())
for _ in range(M):
    s, e = map(int, input().split())
    print(dp[s - 1][e - 1])
