import sys
input = sys.stdin.readline

T = int(input())


def build(graph, node, start, end, N):
    if start == end:
        graph[node] = 1 if start < N else 0
        return

    mid = (start + end) // 2
    build(graph, node * 2, start, mid, N)
    build(graph, node * 2 + 1, mid + 1, end, N)

    graph[node] = graph[node * 2] + graph[node * 2 + 1]

def query(graph,node,start,end,left,right):
    if right < start or left > end:
        return 0
    if left <= start and end <= right:
        return graph[node]

    mid = (start + end) // 2
    return query(graph,node * 2,start,mid,left,right) + query(graph,node * 2 + 1,mid+1,end,left,right)

def update(graph,node,start,end,index,value):
    if start == end:
        graph[node] = value
        return
    mid = (start + end) // 2
    if index <= mid:
        update(graph,node * 2,start,mid,index,value)
    else:
        update(graph,node * 2 + 1,mid+ 1,end,index,value)

    graph[node] = graph[node * 2] + graph[node * 2 + 1]

while T > 0:
    N,M = map(int,input().split())
    seg_tree = [0] * ((N + M) * 4)
    location = [i for i in range(N-1,-1,-1)]
    build(seg_tree,1,0,N+M-1,N)
    count = N - 1
    query_list = list(map(int, input().split()))
    answer = []
    for index in query_list:
        index = index - 1
        answer.append(query(seg_tree,1,0,N+M-1,location[index] + 1,N+M-1))
        update(seg_tree,1,0,N+M-1,location[index],0)
        count+=1
        location[index] = count
        update(seg_tree,1,0,N+M-1,location[index],1)
    print(*answer)
    T-=1
