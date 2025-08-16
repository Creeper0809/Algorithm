import sys
input = sys.stdin.readline

INF = 10**30

def solve_one(n, h, cost):
    allowed = []
    m = len(h)
    for k in range(n - 1):
        S = {h[k][t] - h[k + 1][t] for t in range(m)}
        bad = S & {-1, 0, 1}
        ok = {(u, v) for u in (0, 1) for v in (0, 1) if (v - u) not in bad}
        if not ok:
            return INF
        allowed.append(ok)
    dp0 = [0, cost[0]]
    for i in range(1, n):
        dp1 = [INF, INF]
        for v in (0, 1):
            base = cost[i] * v
            best = INF
            for u in (0, 1):
                if (u, v) in allowed[i - 1] and dp0[u] < best:
                    best = dp0[u]
            dp1[v] = base + best
        dp0 = dp1
    return min(dp0)


t = int(input())
out = []
for _ in range(t):
    n = int(input())
    h = [list(map(int, input().split())) for _ in range(n)]
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    cost_rows = solve_one(n, h, a)
    cost_cols = solve_one(n, list(zip(*h)), b)
    ans = cost_rows + cost_cols
    out.append(str(ans if ans < INF//2 else -1))
print("\n".join(out))