import sys
from collections import defaultdict
input = sys.stdin.readline

arr = defaultdict(int)
N = int(input())
for i in list(map(int, input().split())):
    arr[i] += 1

M = int(input())
result = []
for i in list(map(int, input().split())):
    result.append(arr[i])

print(*result)