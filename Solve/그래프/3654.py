import sys
sys.setrecursionlimit(10**5)
input = sys.stdin.readline

def two_sat(n, clauses):
    def literal_to_id(x):
        var = abs(x) - 1
        return 2 * var + (0 if x > 0 else 1)
    graph = [[] for _ in range(2 * n)]
    for a, b in clauses:
        graph[literal_to_id(-a)].append(literal_to_id(b))
        graph[literal_to_id(-b)].append(literal_to_id(a))
    index = 0
    indices = [-1] * (2 * n)
    lowlink = [0] * (2 * n)
    on_stack = [False] * (2 * n)
    stack = []
    scc_id = [0] * (2 * n)
    scc_count = 0
    def dfs(u):
        nonlocal index, scc_count
        indices[u] = lowlink[u] = index
        index += 1
        stack.append(u)
        on_stack[u] = True
        for v in graph[u]:
            if indices[v] == -1:
                dfs(v)
                lowlink[u] = min(lowlink[u], lowlink[v])
            elif on_stack[v]:
                lowlink[u] = min(lowlink[u], indices[v])
        if lowlink[u] == indices[u]:
            while True:
                v = stack.pop()
                on_stack[v] = False
                scc_id[v] = scc_count
                if v == u:
                    break
            scc_count += 1
    for i in range(2 * n):
        if indices[i] == -1:
            dfs(i)
    for i in range(n):
        if scc_id[2 * i] == scc_id[2 * i + 1]:
            return False
    return True

T = int(input())
for _ in range(T):
    H, W = map(int, input().split())
    grid = [input().strip() for _ in range(H)]
    B_list = []
    num_B = 0
    num_W = 0
    for i in range(H):
        for j in range(W):
            if grid[i][j] == 'B':
                B_list.append((i, j))
                num_B += 1
            elif grid[i][j] == 'W':
                num_W += 1
    if num_B * 2 != num_W:
        print("NO")
        continue

    possible = True
    n = 2 * num_B
    clauses = []

    B_index = {pos: k for k, pos in enumerate(B_list)}

    for k in range(num_B):
        i, j = B_list[k]
        h = k + 1
        v = k + num_B + 1

        left_ok = j > 0 and grid[i][j - 1] == 'W'
        right_ok = j < W - 1 and grid[i][j + 1] == 'W'
        if not left_ok and not right_ok:
            possible = False
        elif not left_ok:
            clauses.append((h, h))
        elif not right_ok:
            clauses.append((-h, -h))

        up_ok = i > 0 and grid[i - 1][j] == 'W'
        down_ok = i < H - 1 and grid[i + 1][j] == 'W'
        if not up_ok and not down_ok:
            possible = False
        elif not up_ok:
            clauses.append((v, v))
        elif not down_ok:
            clauses.append((-v, -v))

    if not possible:
        print("NO")
        continue

    for x in range(H):
        for y in range(W):
            if grid[x][y] != 'W':
                continue
            lits = []
            if y > 0 and grid[x][y - 1] == 'B':
                bk = B_index[(x, y - 1)]
                h_k = bk + 1
                lits.append(h_k)
            if y < W - 1 and grid[x][y + 1] == 'B':
                bk = B_index[(x, y + 1)]
                h_k = bk + 1
                lits.append(-h_k)
            if x > 0 and grid[x - 1][y] == 'B':
                bk = B_index[(x - 1, y)]
                v_k = bk + num_B + 1
                lits.append(v_k)
            if x < H - 1 and grid[x + 1][y] == 'B':
                bk = B_index[(x + 1, y)]
                v_k = bk + num_B + 1
                lits.append(-v_k)
            if len(lits) == 0:
                possible = False
                break
            for i in range(len(lits)):
                for j in range(i + 1, len(lits)):
                    p = lits[i]
                    q = lits[j]
                    clauses.append((-p, -q))

    if not possible:
        print("NO")
        continue

    if two_sat(n, clauses):
        print("YES")
    else:
        print("NO")