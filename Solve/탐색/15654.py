N,M = map(int,input().split())
arr = sorted(list(set(map(int,input().split()))))
answer = []

def back_tracking(depth,num):
    if depth == M:
        print(*answer,sep=" ")
        return
    for i in range(num,len(arr)):
        answer.append(arr[i])
        back_tracking(depth+1,i)
        answer.pop()

back_tracking(0,0)