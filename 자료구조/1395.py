import sys
from collections import deque
import heapq

input = sys.stdin.readline
N,M = map(int,input().split())

seg_tree = [0] * (4*N)
lazy = [0] * (4*N)

def build(node, start, end):
    if start == end:
        seg_tree[node] = 0
        return
    mid = (start+end)//2
    build(2*node,start, mid)
    build(2*node + 1,mid+1, end)
    seg_tree[node] = seg_tree[node * 2] + seg_tree[node * 2 + 1]

def query(node, start, end, left, right):
    update_lazy(node, start, end)
    if left > end or right < start:
        return 0
    if left <= start and end <= right:
        return seg_tree[node]
    mid = (start+end)//2
    return query(2*node,start,mid,left,right) + query(2*node+1,mid+1,end,left,right)

def update_lazy(node, start, end):
    if lazy[node] != 0:
        seg_tree[node] = (end-start+1) - seg_tree[node]
        if start != end:
            lazy[2 * node] ^= 1
            lazy[2 * node + 1] ^= 1
        lazy[node] = 0

def update_range(node, start, end, left, right):
    update_lazy(node, start, end)
    if left > end or right < start:
        return
    if left <= start and end <= right:
        seg_tree[node] = (end-start+1) - seg_tree[node]
        if start != end:
            lazy[2 * node] ^= 1
            lazy[2 * node + 1] ^= 1
        return
    mid = (start+end)//2
    update_range(2*node,start,mid,left,right)
    update_range(2*node+1,mid+1,end,left,right)
    seg_tree[node] = seg_tree[2*node] + seg_tree[2*node+1]

build(1,0,N-1)
for _ in range(M):
    query_arr = list(map(int,input().split()))
    if query_arr[0] == 0:
        update_range(1,0,N-1,query_arr[1]-1,query_arr[2]-1)
    else:
        print(query(1,0,N-1,query_arr[1]-1,query_arr[2]-1))

