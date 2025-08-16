import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    sx = 0
    sp = 0
    for _ in range(n):
        x, y = map(int, input().split())
        sx ^= x
        sp ^= x + y
    print(sx, sp - sx)
