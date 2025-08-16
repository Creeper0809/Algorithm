import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline
size = 10 ** 6 + 1
seg_tree = [0] * (4*size)

def update(node, start, end, index, value):
    if start == end:
        seg_tree[node] += value
        return
    mid = (start+end)//2
    if index <= mid:
        update(2*node,start,mid,index,value)
    else:
        update(2*node+1,mid+1,end,index,value)
    seg_tree[node] = seg_tree[node * 2] + seg_tree[node * 2 + 1]

def query(node, start, end, rank):
    if start == end:
        return start
    mid = (start+end)//2
    left = seg_tree[node * 2]
    if left >= rank:
        return query(2*node,start,mid,rank)
    else:
        return query(2*node + 1,mid + 1,end,rank - left)

for _ in range(int(input())):
    temp = list(map(int, input().split()))
    if temp[0] == 1:
        index = query(1,0,size-1,temp[1])
        print(index)
        update(1, 0, size - 1, index, -1)
    else:
        update(1,0,size-1,temp[1],temp[2])