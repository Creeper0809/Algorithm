import sys
sys.setrecursionlimit(100000)
input = sys.stdin.readline

T = int(input())
for cas in range(1, T + 1):
    N, K = map(int, input().split())
    children = [[] for _ in range(N + 1)]
    for i in range(2, N + 1):
        p, c = map(int, input().split())
        children[p].append((i, c))

    INF = 10**18
    dp = [[-INF] * (K + 1) for _ in range(N + 1)]

    def dfs(u):
        if not children[u]:
            dp[u][0] = 0
            if u != 1:
                dp[u][1] = 0
            return

        curr = [-INF] * (K + 1)
        curr[0] = 0
        for v, cv in children[u]:
            dfs(v)
            new_curr = [-INF] * (K + 1)
            for prev in range(K + 1):
                if curr[prev] == -INF:
                    continue
                for jv in range(K - prev + 1):
                    if dp[v][jv] == -INF:
                        continue
                    min_val = min(jv, K - jv + 1)
                    add = dp[v][jv] + cv * min_val
                    new_curr[prev + jv] = max(new_curr[prev + jv], curr[prev] + add)
            curr = new_curr

        for j in range(K + 1):
            if curr[j] != -INF:
                dp[u][j] = max(dp[u][j], curr[j])
                if u != 1 and j + 1 <= K:
                    dp[u][j + 1] = max(dp[u][j + 1], curr[j])

    dfs(1)
    ans = 2 * dp[1][K] if dp[1][K] != -INF else 0
    print(f"Case {cas}: {ans}")