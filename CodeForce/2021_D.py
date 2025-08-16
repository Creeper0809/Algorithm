import sys

input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

MOD = 10 ** 9 + 7

t = int(input())
for _ in range(t):
    n, m, k = map(int, input().split())
    points = [tuple(map(lambda x: int(x) - 1, input().split())) for _ in range(k + 1)]

    fixed = set(points)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    dp = [{} for _ in range(k + 1)]  # dp[i][used_set as tuple] = 경우의 수

    # 초기 상태
    dp[0][tuple()] = 1

    for i in range(k):
        x1, y1 = points[i]
        x3, y3 = points[i + 1]

        if abs(x1 - x3) + abs(y1 - y3) != 2:
            dp[i + 1] = {}
            break

        for used_tuple in dp[i]:
            used_now = set(used_tuple)

            candidates = []
            for dx, dy in dirs:
                nx, ny = x1 + dx, y1 + dy
                if 0 <= nx < n and 0 <= ny < m:
                    if (nx, ny) not in fixed and (nx, ny) not in used_now:
                        if abs(nx - x3) + abs(ny - y3) == 1:
                            candidates.append((nx, ny))

            if not candidates:
                continue

            for nx, ny in candidates:
                new_used = tuple(sorted(used_now | {(nx, ny)}))
                if new_used not in dp[i + 1]:
                    dp[i + 1][new_used] = 0
                dp[i + 1][new_used] = (dp[i + 1][new_used] + dp[i][used_tuple]) % MOD

    ans = sum(dp[k].values()) % MOD
    print(ans)
