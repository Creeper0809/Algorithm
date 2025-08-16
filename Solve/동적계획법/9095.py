import sys
input = sys.stdin.readline

T = int(input())
test_cases = [int(input()) for _ in range(T)]

max_n = max(test_cases)

dp = [0] * (max_n + 3)
dp[0] = 1
dp[1] = 1
dp[2] = 2

for i in range(3, max_n + 1):
    dp[i] = dp[i-1] + dp[i-2] + dp[i-3]

for n in test_cases:
    print(dp[n])