import heapq
import sys

input = sys.stdin.readline

arr = []
N = int(input())

for _ in range(N):
    num = int(input())
    if num == 0:
        print(heapq.heappop(arr)[1] if arr else 0)
        continue
    heapq.heappush(arr, (abs(num),num))