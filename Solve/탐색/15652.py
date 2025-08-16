N,M = map(int,input().split())

answer = []
def back_track(length,num):
    if length == M:
        print(*answer , sep=" ")
        return
    for i in range(num,N+1):
        answer.append(i)
        back_track(length + 1,i)
        answer.pop()


back_track(0,1)
