N,D,K = map(int,input().split())

arr = [0 for _ in range(N)]
arr2 = list(map(int,input().split()))
answer = 0
for _ in range(D):
    flag = False
    for i in range(N):
        if arr[i] + arr2[i] > K:
            flag = True
            break
    if flag:
        arr = [0 for _ in range(N)]
        answer += 1
    arr = [arr[i] + arr2[i] for i in range(N)]
print(answer)