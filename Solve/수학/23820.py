N = int(input())
arr = list(map(int,input().split()))
bits = 0
for i in arr:
    bits |= (1<<i)
answer = 0
while bits & (1 << answer):
    answer += 1
print(answer)