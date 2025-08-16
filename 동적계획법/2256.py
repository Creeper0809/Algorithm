import sys
input = sys.stdin.readline

def solve():
    k, n = map(int, input().split())
    chopstick = list()
    for _ in range(n):
        chopstick.append(int(input()))
    chopstick.sort()
    INF = 10 ** 18
    dp = [[INF] * (n + 2) for _ in range(k + 1)]
    for j in range(n + 2):
        dp[0][j] = 0
    for i in range(1, k + 1):
        max_j = n - (3 * i)
        for j in range(max_j, -1, -1):
            cost = (chopstick[j + 1] - chopstick[j]) ** 2
            dp[i][j] = min(dp[i][j + 1], dp[i - 1][j + 2] + cost)
    print(dp[k][0])
solve()
