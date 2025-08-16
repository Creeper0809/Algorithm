R,C = map(int,input().split())
panja = [list(input()) for _ in range(R)]
visited = [[False] * C for _ in range(R)]
def dfs(start,deco):
    r,c = start
    if deco == "|":
        if 0<=r+1<R and panja[r+1][c] == "|":
            dfs((r+1,c),deco)
            visited[r+1][c] = True
    else:
        if 0<=c+1<C and panja[r][c+1] == "-":
            dfs((r,c+1),deco)
            visited[r][c + 1] = True

answer = 0
for i in range(R):
    for j in range(C):
        if not visited[i][j]:
            dfs((i,j),panja[i][j])
            answer += 1
print(answer)