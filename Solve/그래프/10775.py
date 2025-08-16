N = int(input())
M = int(input())
parent = [i for i in range(N+1)]

def find(x):
    if parent[x] == x:
        return parent[x]
    y = find(parent[x])
    parent[x] = y
    return y

def union(x,y):
    root1 = find(x)
    root2 = find(y)

    if root1<root2:
        parent[root2] = root1
    else:
        parent[root1] = root2
count = 0
for _ in range(N):
    num = int(input())
    root = find(num)
    if root != 0:
        union(root,root-1)
        count+=1
    else:
        break

print(count)