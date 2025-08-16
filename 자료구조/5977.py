import sys
from collections import deque

input = sys.stdin.readline
N,K = map(int,input().split())
arr = list()
for _ in range(N):
    arr.append(int(input()))

Psum = list()
sum_temp = 0
for i in arr:
    Psum.append(sum_temp+i)
    sum_temp += i
dp = [0] * (N+1)
queue = deque()

def get_value(index):
    return dp[index - 1] - Psum[index]

for index in range(N):
    while queue and queue[0] < index - K:
        queue.popleft()
    while queue and get_value(queue[-1]) < get_value(index):
        queue.pop()
    queue.append(index)
    dp[index] = Psum[index] + get_value(queue[0])
    if index < K:
        dp[index] = Psum[index]

print(dp[N-1])
