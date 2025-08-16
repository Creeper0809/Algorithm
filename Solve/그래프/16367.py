import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

k, n = map(int, input().split())
N = 2 * k
g = [[] for _ in range(N)]

def var(lamp, val):
    return 2 * lamp + val

for _ in range(n):
    tokens = input().split()
    wrong = []
    for i in range(0, 6, 2):
        lamp = int(tokens[i]) - 1
        guess = tokens[i+1]
        if guess == 'R':
            wrong.append(var(lamp, 0))
        else:
            wrong.append(var(lamp, 1))
    for i in range(3):
        for j in range(i+1, 3):
            A = wrong[i]
            B = wrong[j]
            notA = A ^ 1
            notB = B ^ 1
            g[A].append(notB)
            g[B].append(notA)

index = 0
stack = []
onstack = [False] * N
indices = [-1] * N
lowlink = [0] * N
comp = [-1] * N
cid = 0

def dfs(v):
    global index, cid
    indices[v] = lowlink[v] = index
    index += 1
    stack.append(v)
    onstack[v] = True
    for w in g[v]:
        if indices[w] == -1:
            dfs(w)
            lowlink[v] = min(lowlink[v], lowlink[w])
        elif onstack[w]:
            lowlink[v] = min(lowlink[v], indices[w])
    if lowlink[v] == indices[v]:
        while True:
            w = stack.pop()
            onstack[w] = False
            comp[w] = cid
            if w == v:
                break
        cid += 1

for v in range(N):
    if indices[v] == -1:
        dfs(v)

ans = []
for i in range(k):
    if comp[2*i] == comp[2*i+1]:
        print(-1)
        sys.exit()
    ans.append('R' if comp[2*i] > comp[2*i+1] else 'B')

print(''.join(ans))
