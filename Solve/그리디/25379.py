lcount = 0
rcount = 0
count = 0
value = 0
N = int(input())
nums = list(map(int,input().split()))
for i in range(0,N):
    if nums[i] % 2 == 0:
        count += value
        lcount += i
        rcount += N - i - 1
        value += 1
print(min(lcount,rcount)-count)