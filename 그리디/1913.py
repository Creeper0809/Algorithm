N = int(input())
arr = list()
for _ in range(N):
    start,end = map(int,input().split())
    arr.append((start,end))

arr.sort(key=lambda x : (x[1],x[0]))

endtime = 0
answer = 0
for start,end in arr:
    if endtime <= start:
        endtime = end
        answer += 1
print(answer)
