import sys
N, K = map(int, sys.stdin.readline().split())
arr = [int(sys.stdin.readline()) for _ in range(N)]
answer = 0
for i in reversed(arr):
    answer += K // i
    K %= i
print(answer)
