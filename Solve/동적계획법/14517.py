import sys
sys.setrecursionlimit(10**6)
string = input()
string_len = len(string)
mod = 10**4 + 7
dp = [[-1] * string_len  for _ in range(string_len)]

def solve(i, j):
    if dp[i][j] != -1:
        return dp[i][j] % mod
    if i == j:
        return 1
    elif i > j:
        return 0
    dp[i][j] = (solve(i+1, j) + solve(i, j-1) - solve(i+1, j-1))%mod
    if string[i] == string[j]:
        dp[i][j] = (dp[i][j] + solve(i+1, j-1) + 1)%mod
    return dp[i][j]
print(solve(0, string_len-1) % mod)