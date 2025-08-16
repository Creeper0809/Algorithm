N,r,c = map(int,input().split())

def zSearch(N,r,c):
    if N == 0:
        return 0
    return 4*zSearch(N-1,r//2,c//2) + 2*(r%2) + (c%2)

print(zSearch(N,r,c))