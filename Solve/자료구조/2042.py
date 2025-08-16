import sys
input = sys.stdin.readline

N,M,K = map(int,input().split())
arr = list()
for _ in range(N):
    arr.append(int(input()))

seg_tree = [0] * (4*N)

def build(node, start, end):
    if start == end:
        seg_tree[node] = arr[start]
        return
    mid = (start+end)//2
    build(2*node,start, mid)
    build(2*node + 1,mid+1, end)
    seg_tree[node] = seg_tree[node * 2] + seg_tree[node * 2 + 1]

def query(node, start, end, left, right):
    if left > end or right < start:
        return 0
    if left <= start and end <= right:
        return seg_tree[node]
    mid = (start+end)//2
    return query(2*node,start,mid,left,right) + query(2*node+1,mid+1,end,left,right)

def update(node, start, end, index, value):
    if start == end:
        seg_tree[node] = value
        return
    mid = (start+end)//2
    if index <= mid:
        update(2*node,start,mid,index,value)
    else:
        update(2*node+1,mid+1,end,index,value)
    seg_tree[node] = seg_tree[2*node] + seg_tree[2*node+1]

build(1,0,N-1)

for _ in range(M + K):
    query_type, a, b = map(int,input().split())
    if query_type == 1:
        update(1,0,N-1,a-1,b)
    else:
        print(query(1,0,N-1,a-1,b-1))
