import sys

input = sys.stdin.readline
N,M = map(int,input().rstrip().split())
nums = list(map(int,input().rstrip().split()))
sums = [0] * (N+1)
for i in range(1,len(sums)):
    sums[i] = sums[i-1] + nums[i-1]


for _ in range(M):
    i,j = map(int,input().rstrip().split())
    print(sums[j] - sums[i-1])
