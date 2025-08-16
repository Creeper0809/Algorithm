N = int(input())
arr = list(map(int, input().split()))
arr.sort()
min_sum = 1e20
answer = []
for i in range(N - 2):
    left = i + 1
    right = N - 1

    while left < right:
        sum = arr[left] + arr[right] + arr[i]

        if abs(sum) < min_sum:
            answer = [arr[i], arr[left], arr[right]]
            min_sum = abs(sum)
        if sum == 0:
            break
        if sum < 0:
            left += 1
        else:
            right -= 1

print(*sorted(answer), sep=" ")