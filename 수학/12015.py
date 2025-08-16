import bisect
import copy

x = int(input())
arr = list(map(int, input().split()))

dp = [arr[0]]
answer = []
total_len = 0
for i in range(x):
    if arr[i] > dp[-1]:
        dp.append(arr[i])
        answer = copy.deepcopy(dp)
    else:
        idx = bisect.bisect_left(dp, arr[i])
        dp[idx] = arr[i]


print(len(dp))
print(*answer,sep=" ")