import sys
from collections import deque
import heapq

input = sys.stdin.readline

N = int(input())
arr = list(map(int,input().split()))
seg_tree = [0] * (4*N)
lazy = [0] * (4*N)

def build(node, start, end):
    if start == end:
        seg_tree[node] = arr[start]
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
        seg_tree[node] += (end -start+1) * lazy[node]
        if start != end:
            lazy[2*node] += lazy[node]
            lazy[2*node + 1] += lazy[node]
        lazy[node] = 0

def update_range(node, start, end, left, right, value):
    update_lazy(node, start, end)
    if left > end or right < start:
        return
    if left <= start and end <= right:
        seg_tree[node] += (end -start+1) * value
        if start != end:
            lazy[2*node] += value
            lazy[2*node + 1] += value
        return
    mid = (start+end)//2
    update_range(2*node,start,mid,left,right,value)
    update_range(2*node+1,mid+1,end,left,right,value)
    seg_tree[node] = seg_tree[2*node] + seg_tree[2*node+1]

build(1,0,N-1)

M = int(input())
for _ in range(M):
    query_arr = list(map(int,input().split()))
    if query_arr[0] == 1:
        update_range(1,0,N-1,query_arr[1]-1,query_arr[2]-1,query_arr[3])
    else:
        print(query(1,0,N-1,query_arr[1]-1,query_arr[1]-1))

