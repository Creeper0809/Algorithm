import sys

input = sys.stdin.readline
sys.setrecursionlimit(10 ** 5)

n = int(input())
tree = [[] for _ in range(n + 1)]
for _ in range(n):
    templist = list(map(int,input().split()))
    parent = templist[0]
    for i in range(1,len(templist),2):
        child = templist[i]
        if child == -1:
            break
        weight = templist[i+1]
        tree[parent].append((child, weight))


tempcost = 0
visited = [False] * (n+1)
distance = [0] * (n+1)
def DFS(node, cost):
    global tempnode
    global tempcost
    visited[node] = True
    for adj_node, adj_w in tree[node]:
        cal_w = cost + adj_w
        if not visited[adj_node]:
            distance[adj_node] = cal_w
            if tempcost < cal_w:
                tempnode = adj_node
                tempcost = cal_w
            DFS(adj_node, cal_w)

DFS(1, 0)
rootnode = tempnode
tempcost = 0
visited = [False] * (n+1)
distance = [0] * (n+1)
DFS(rootnode, 0)
print(max(distance))