import sys
input = sys.stdin.readline

N,M = map(int,input().split())
arr = [[sys.maxsize,-1] for _ in range(N+1)]
for _ in range(M):
    node,start,end = map(int,input().split())
    min_start,max_end = arr[node]
    if not (min_start<start<max_end or min_start<end<max_end):
        arr[node] = [min(min_start,start),max(max_end,end)]
        print("YES")
    else:
        print("NO")