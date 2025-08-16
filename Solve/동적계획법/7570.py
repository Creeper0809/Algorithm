N = int(input())
arr = list(map(int,input().split()))

dp = [0] * (N+1)

for i in arr:
    dp[i] = dp[i-1]+1
# dp[5] = dp[4] + 1 == [0,0,0,0,1]
# dp[2] = dp[1] + 1 == [0,1,0,0,1]
# dp[4] = dp[3] + 1 == [0,1,0,1,1]
# dp[1] = dp[0] + 1 == [1,1,0,1,1]
# dp[3] = dp[2] + 1 == [1,1,2,1,1]
dp = [0] * (N+1)



#lis 최장 증가 수열 길이
for i in range(N):
    dp[i] = 1
    for j in range(i):
        print(i,"번째 i수:",arr[i],j,"번째 j수",arr[j])
        if arr[i] > arr[j]:
            print(dp[i], dp[j])
            dp[i] = max(dp[j]+1,dp[i])
print(dp)