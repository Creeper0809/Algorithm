N,M = map(int,input().split())
parent = [i for i in range(N+1)]
know_Truth = [False] * (N+1)

arr = list(map(int,input().split()))

for i in arr[1:]:
    know_Truth[i] = True

def find(x):
    if parent[x] == x:
        return parent[x]
    y = find(parent[x])
    parent[x] = y
    return y

def union(x,y):
    root1 = find(x)
    root2 = find(y)

    if know_Truth[root1]:
        parent[root2] = parent[root1]
    elif know_Truth[root2]:
        parent[root1] = parent[root2]
    else:
        parent[root1] = parent[root2]

parties = []

for _ in range(M):
    party = list(map(int,input().split()))[1:]
    parties.append(party)
    person = party[0]
    for i in range(1,len(party)):
        union(person,party[i])

count = 0
for i in parties:
    if not know_Truth[find(i[0])]:
        count += 1
print(count)

