import sys
sys.setrecursionlimit(10**6)

def tarjan_scc(graph):
    n = len(graph)
    id = 0
    ids = [-1] * n
    low = [0] * n
    on_stack = [False] * n
    stack = []
    sccs = []
    scc_id = [0] * n
    def dfs(at):
        nonlocal id
        ids[at] = low[at] = id
        id += 1
        stack.append(at)
        on_stack[at] = True

        for to in graph[at]:
            if ids[to] == -1:
                dfs(to)
                low[at] = min(low[at], low[to])
            elif on_stack[to]:
                low[at] = min(low[at], ids[to])

        if ids[at] == low[at]:
            scc = []
            while True:
                node = stack.pop()
                on_stack[node] = False
                scc.append(node)
                scc_id[node] = len(sccs)
                if node == at:
                    break
            sccs.append(scc)

    for i in range(n):
        if ids[i] == -1:
            dfs(i)

    return sccs

# 입력 처리
N, M = map(int, input().split())
graph = [[] for _ in range(N)]

for _ in range(M):
    A, B = map(int, input().split())
    graph[A - 1].append(B - 1)

sccs = tarjan_scc(graph)
for i in range(len(sccs)):
    sccs[i] = sorted(sccs[i])
sccs.sort(key=lambda x: x[0])
print(len(sccs))
for scc in sccs:
    scc = sorted([i + 1 for i in scc])
    scc.append(-1)
    print(*scc)
