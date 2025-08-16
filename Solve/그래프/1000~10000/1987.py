import sys
# 아스키 코드로 풀어야 하는걸 봤다
input = sys.stdin.readline
R,C = list(map(int,input().split()))
miro = [list(map(lambda x: ord(x)-65, sys.stdin.readline().rstrip())) for _ in range(R)]
dir = [[1,0],[-1,0],[0,-1],[0,1]]

alphabet = [0] * 26

max = 0
def dfs(pos,count):
    global max
    if count > max:
        max = count
    r,c = pos
    for dr,dc in dir:
        ddr = dr + r
        ddc = dc + c
        if 0<=ddr<R and 0<=ddc<C and alphabet[miro[ddr][ddc]] == 0:
            alphabet[miro[ddr][ddc]] = 1
            dfs((ddr,ddc),count + 1)
            alphabet[miro[ddr][ddc]] = 0


alphabet[miro[0][0]] = 1
dfs((0,0),1)
print(max)