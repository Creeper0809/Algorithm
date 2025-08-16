import sys
from collections import deque
import heapq

input = sys.stdin.readline

N = int(input())
arr = list(map(int,input().split()))
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
    seg_tree[node] = seg_tree[node * 2] + seg_tree[node * 2 + 1]

build(1,0,N-1)

M = int(input())
query_list = list()
update_list = deque()
for i in range(M):
    phrase = list(map(int,input().split()))
    if phrase[0] == 1:
        update_list.append(phrase[1:])
    else:
        heapq.heappush(query_list,[phrase[1],i,phrase[2],phrase[3]])

count = 0
query_result = list()
while True:
    while query_list:
        next_query = heapq.heappop(query_list)
        if next_query[0] != count:
            heapq.heappush(query_list, next_query)
            break
        heapq.heappush(query_result, [next_query[1], query(1, 0, N - 1, next_query[2] - 1, next_query[3] - 1)])
    if not update_list:
        break
    next_update = update_list.popleft()
    update(1,0,N-1,next_update[0]-1,next_update[1])
    count += 1

while query_result:
    print(heapq.heappop(query_result)[1])
