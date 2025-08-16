n = int(input())
arr = [list(map(int, input().split())) for _ in range(n)]
wasSame = [[0]*n for _ in range(n)]
for i in range(5):
    for j in range(n):
        for k in range(j+1,n):
            if arr[j][i] == arr[k][i]:
                wasSame[k][j] = 1
                wasSame[j][k] = 1
countSame = []
for i in wasSame:
    countSame.append(i.count(1))
print(countSame.index(max(countSame))+1)

