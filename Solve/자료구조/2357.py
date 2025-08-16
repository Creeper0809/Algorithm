import sys;input=sys.stdin.readline

N,M = map(int,input().split())
arr = list()

for _ in range(N):
    arr.append(int(input()))

min_seg = [0] * (4*N)
max_seg = [0] * (4*N)

def init(arr,target_arr,node,start,end,func):
    if start == end:
        target_arr[node] = arr[start]
        return
    mid = start + (end-start)//2
    init(arr,target_arr,node*2,start,mid,func)
    init(arr, target_arr, node * 2 + 1, mid + 1, end, func)
    target_arr[node] = func(target_arr[node*2],target_arr[node*2+1])

def query(target_arr,node,start,end,left,right,func):
    if left > end or right < start:
        return -1
    if left <= start and end <= right:
        return target_arr[node]
    mid = start + (end-start)//2
    lfunc = query(target_arr,node*2,start,mid,left,right,func)
    rfunc = query(target_arr,node*2+1,mid+1,end,left,right,func)
    if lfunc == -1:
        return rfunc
    elif rfunc == -1:
        return lfunc
    else:
        return func(lfunc,rfunc)

init(arr,min_seg,1,0,N-1,min)
init(arr,max_seg,1,0,N-1,max)

for _ in range(M):
    left,right = map(int,input().split())
    print(query(min_seg,1,0,N-1,left-1,right-1,min), query(max_seg,1,0,N-1,left-1,right-1,max))
