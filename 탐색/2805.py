N,M = map(int,input().split())
trees = list(map(int,input().split()))
lo,hi = -1,1_000_000_000

while lo+1 < hi:
    mid = (lo+hi)//2
    if sum(tree - mid for tree in trees if tree > mid) < M:
        hi = mid
    else:
        lo = mid
print(lo)