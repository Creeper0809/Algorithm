import sys
from collections import deque
sys.setrecursionlimit(1000000)
input=sys.stdin.readline
INF_CAP=10**9
class Edge:
    __slots__=('dest','capacity','rev')
    def __init__(self,dest,capacity,rev):
        self.dest=dest
        self.capacity=capacity
        self.rev=rev

def add_edge(adj_list,from_node,to_node,capacity_map,flow_map):
    cap=capacity_map[(from_node,to_node)]
    adj_list[from_node].append(Edge(to_node,cap,len(adj_list[to_node])))
    adj_list[to_node].append(Edge(from_node,0,len(adj_list[from_node])-1))
    flow_map[(from_node,to_node)]=0
    flow_map[(to_node,from_node)]=0

def build_level_graph(adj_list,start,end,level):
    for i in range(len(level)):level[i]=-1
    dq=deque([start]);level[start]=0
    while dq:
        u=dq.popleft()
        for e in adj_list[u]:
            if level[e.dest]<0 and e.capacity>0:
                level[e.dest]=level[u]+1
                dq.append(e.dest)
    return level[end]>=0

def send_flow(adj_list,node,sink,flow_limit,level,it):
    if node==sink:return flow_limit
    while it[node]<len(adj_list[node]):
        e=adj_list[node][it[node]]
        if e.capacity>0 and level[node]<level[e.dest]:
            pushed=send_flow(adj_list,e.dest,sink,min(flow_limit,e.capacity),level,it)
            if pushed>0:
                e.capacity-=pushed
                adj_list[e.dest][e.rev].capacity+=pushed
                return pushed
        it[node]+=1
    return 0

def compute_max_flow(adj_list,source,sink):
    total_flow=0
    n=len(adj_list)
    level=[0]*n
    while build_level_graph(adj_list,source,sink,level):
        it=[0]*n
        while True:
            pushed=send_flow(adj_list,source,sink,INF_CAP,level,it)
            if pushed==0:break
            total_flow+=pushed
    return total_flow

total_rows,total_cols=map(int,input().split())
grid=[input().rstrip() for _ in range(total_rows)]
start_row=start_col=end_row=end_col=-1
for r in range(total_rows):
    for c in range(total_cols):
        if grid[r][c]=='K':start_row,start_col=r,c
        if grid[r][c]=='H':end_row,end_col=r,c
if abs(start_row-end_row)+abs(start_col-end_col)==1:
    print(-1);sys.exit()
total_cells=total_rows*total_cols
total_nodes=total_cells*2+2
source_node=total_nodes-2
sink_node=total_nodes-1
adj_list=[[] for _ in range(total_nodes)]
capacity={}
flow_map={}
dirs=[(1,0),(-1,0),(0,1),(0,-1)]
for r in range(total_rows):
    for c in range(total_cols):
        if grid[r][c]=='#':continue
        idx=r*total_cols+c
        in_node=idx*2
        out_node=in_node+1
        cap=INF_CAP if grid[r][c] in('K','H') else 1
        capacity[(in_node,out_node)]=cap
        capacity[(out_node,in_node)]=0
        add_edge(adj_list,in_node,out_node,capacity,flow_map)
        for dr,dc in dirs:
            nr,ni=r+dr,c+dc
            if 0<=nr<total_rows and 0<=ni<total_cols and grid[nr][ni]!='#':
                nidx=nr*total_cols+ni
                capacity[(out_node,nidx*2)]=INF_CAP
                capacity[(nidx*2,out_node)]=0
                add_edge(adj_list,out_node,nidx*2,capacity,flow_map)
        if grid[r][c]=='K':
            capacity[(source_node,in_node)]=INF_CAP
            capacity[(in_node,source_node)]=0
            add_edge(adj_list,source_node,in_node,capacity,flow_map)
        if grid[r][c]=='H':
            capacity[(out_node,sink_node)]=INF_CAP
            capacity[(sink_node,out_node)]=0
            add_edge(adj_list,out_node,sink_node,capacity,flow_map)
res=compute_max_flow(adj_list,source_node,sink_node)
print(res)
