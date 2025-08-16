import sys
input = sys.stdin.readline
N = int(input())

A,B = 0,0
for _ in range(N):
    a,b = map(int,input().split())
    A += a
    B += b
    print(A-B)