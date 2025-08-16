from collections import deque;b=[deque(map(int,input()))for _ in range(4)]
def r(n,m,a):
    if n in a:
        return
    a.append(n)
    if n+1<4 and b[n][2]!=b[n+1][6]:
        r(n+1,-m,a)
    if n-1>-1 and b[n][6]!=b[n-1][2]:
        r(n-1,-m, a)
    b[n].rotate(m)
for _ in range(int(input())):
    n,m=map(int,input().split())
    r(n-1,m,[])
print(sum([b[i][0]*2**i for i in range(4)]))