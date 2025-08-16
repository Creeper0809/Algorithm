import sys
sys.setrecursionlimit(10**6)
class Node:
    def __init__(self):
        self.child = {}

root_node = Node()

def insert(words):
    node = root_node
    for i in words:
        if i not in node.child:
            node.child[i] = Node()
        node = node.child[i]

N = int(input())
for i in range(N):
    words = input().split()
    insert(words[1:])

def dfs(node,depth):
    for key,value in sorted(node.child.items()):
        print(("--" * depth) + key)
        dfs(value,depth+1)

dfs(root_node,0)



