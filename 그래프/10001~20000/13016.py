import sys

input = sys.stdin.readline
sys.setrecursionlimit(10 ** 5)

n = int(input())
tree = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    parent, child, weight = map(int, input().split())
    tree[parent].append((child, weight))
    tree[child].append((parent, weight))

tempnode = 0
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
rootDistance = distance.copy()
#print("루트 노드:",rootnode,rootDistance)

visited = [False] * (n+1)
distance = [0] * (n+1)
tempcost = 0
tailnode = tempnode
DFS(tailnode, 0)
tailDistance = distance.copy()
#print("꼬리 노드",tailnode,tailDistance)

for i in range(1,n+1):
    print(max(tailDistance[i],rootDistance[i]))