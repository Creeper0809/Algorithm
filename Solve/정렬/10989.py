import sys
input = sys.stdin.readline
N = int(input())
arr = list()
for _ in range(N):
    arr.append(int(input()))
arr.sort()
for i in arr:
    print(i)