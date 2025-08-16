import sys
from collections import deque

input = sys.stdin.readline
dir1 = [[0, 1], [1, 0], [0, -1], [-1, 0]]
dir2 = [[1, 0], [0, 1], [-1, 0], [0, -1],[1,1],[-1,-1],[-1,1],[1,-1]]

def multi_source_bfs(sources, M, N, graph,find,direction):
    vis = [[0] * M for _ in range(N)]
    dq = deque(sources)
    for i, j in sources:
        vis[i][j] = 1
    while dq:
        i, j = dq.popleft()
        for di, dj in direction:
            ni, nj = i + di, j + dj
            if 0 <= ni < N and 0 <= nj < M and graph[ni][nj] == find and not vis[ni][nj]:
                vis[ni][nj] = 1
                dq.append((ni, nj))
    return vis


def build_prefix_sum(grid, N, M):
    S = [[0] * (M + 1) for _ in range(N + 1)]
    for i in range(N):
        row_sum = 0
        for j in range(M):
            row_sum += grid[i][j]
            S[i + 1][j + 1] = S[i][j + 1] + row_sum
    return S

def clamp(x, lo, hi):
    return max(lo, min(x, hi))

def safe_query(S, r1, c1, r2, c2, N, M):
    r1 = clamp(r1, 0, N - 1)
    c1 = clamp(c1, 0, M - 1)
    r2 = clamp(r2, 0, N - 1)
    c2 = clamp(c2, 0, M - 1)
    if r1 > r2 or c1 > c2:
        return 0
    return S[r2 + 1][c2 + 1] - S[r1][c2 + 1] - S[r2 + 1][c1] + S[r1][c1]


def solve_test(M, N, graph):
    num_arr = multi_source_bfs([(0, 0)], M, N, graph,'.',dir1)

    ru_sources = []
    ld_sources = []

    for j in range(M - 1):
        if num_arr[0][j] == 0:
            ru_sources.append((0, j))
        if num_arr[N - 1][j] == 0:
            ld_sources.append((N - 1, j))
    for i in range(N - 1):
        if num_arr[i][M - 1] == 0:
            ru_sources.append((i, M - 1))
        if num_arr[i][0] == 0:
            ld_sources.append((i, 0))

    right_up = multi_source_bfs(ru_sources, M, N, num_arr,0,dir2)
    left_down = multi_source_bfs(ld_sources, M, N, num_arr,0,dir2)

    num_arr[N - 1][M - 1] = 0
    right_prefix = build_prefix_sum(right_up, N, M)
    down_prefix = build_prefix_sum(left_down, N, M)
    install_prefix = build_prefix_sum(num_arr, N, M)

    ans = sys.maxsize
    ans_i = ans_j = -1
    for i in range(N):
        for j in range(M):
            if (i == 0 and j == 0) or (i == N - 1 and j == M - 1) or num_arr[i][j] != 1:
                continue
            limit = min(M - j, N - i)
            lo,hi = -1,limit
            while lo + 1 < hi:
                mid = (lo + hi) // 2

                is_right_up = j + mid == M - 1 or (safe_query(right_prefix, i - 1, j - 1, i + mid + 1, j + mid + 1, N, M) > 0)
                is_left_down =  i + mid == N - 1 or (safe_query(down_prefix, i - 1, j - 1, i + mid + 1, j + mid + 1, N, M) > 0)

                if (is_left_down and is_right_up) or (is_right_up and j == 0) or (is_left_down and i == 0):
                    hi = mid
                else:
                    lo = mid

            need_block = lo + 2

            if ans < need_block:
                continue

            lo,hi = -1,limit

            while lo + 1 < hi:
                mid = (lo + hi) // 2
                total = safe_query(install_prefix, i, j, i + mid, j + mid, N, M)
                if total == (mid + 1) ** 2:
                    lo = mid
                else:
                    hi = mid

            max_install = lo + 1

            if max_install >= need_block:
                if ans > need_block:
                    ans = need_block
                    ans_i, ans_j = i, j

    if ans == sys.maxsize:
        return "Impossible"
    else:
        return f"{ans} {ans_j + 1} {ans_i + 1}"

N, M = map(int, input().split())
graph = [list(input()) for _ in range(M)]
print(solve_test(N, M, graph))