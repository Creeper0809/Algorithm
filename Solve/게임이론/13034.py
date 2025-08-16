import sys
input = sys.stdin.readline

N = int(input())

g = [0] * (N + 1)
if N >= 2:
    g[2] = 1

for i in range(3, N + 1):
    visited = [False] * i
    for left in range(i // 2 + 1):
        right = i - 2 - left
        x = g[left] ^ g[right]
        if x < i:
            visited[x] = True
    mex = 0
    while visited[mex]:
        mex += 1
    g[i] = mex

print(1 if g[N] != 0 else 2)
