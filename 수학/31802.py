n = int(input())
nums = list(map(int, input().split()))
left, right = map(int, input().split())

if left > right:
    left, right = right, left

if left == right:
    print(0)
    exit()

a = right - left
m = a // n
r = a % n

result = sum(nums) * m
left = left % n
for i in range(r):
    result += nums[(left + i) % n]

print(result)
