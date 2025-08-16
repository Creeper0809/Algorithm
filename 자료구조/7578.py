import sys
input = sys.stdin.readline

N = int(input())
a_pos = list(map(int,input().split()))
b_pos = {}
for i,element in enumerate(list(map(int,input().split()))):
    b_pos[element] = i

seg_tree = [0] * (4*N)

def build(node, start, end):
    if start == end:
        seg_tree[node] = 0
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
    seg_tree[node] = seg_tree[node * 2] + seg_tree[node * 2 + 1]

build(1,0,N-1)
answer = 0
for i in range(N):
    pos = b_pos[a_pos[i]]
    answer += query(1,0,N-1,pos,N-1)
    update(1,0,N-1,pos,1)
print(answer)