N,M = map(int,input().split())

arr = list()
for i in range(N):
    arr.append(list())
    for j in input():
        arr[i].append(j)

for x in range(M):
    flag = True
    for j in range(N):
        if arr[j][x] == 'O':
            flag = False
            break
    if flag:
        print(x + 1)
        exit(0)

print("ESCAPE FAILED")