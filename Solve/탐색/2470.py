N = int(input())
arr = list(map(int,input().split()))
arr.sort()
left,right = 0,N-1
min_sum = 1e12
answer = []
while left < right:
    sum = arr[left] + arr[right]

    if abs(sum) < min_sum:
        answer = [arr[left],arr[right]]
        min_sum = abs(sum)
    if sum == 0:
        break
    if sum < 0:
        left += 1
    else:
        right -= 1

print(*answer,sep=" ")