N = int(input())
stones = list(map(int,input().split()))

grundy_num = 0
for i in stones:
    grundy_num ^= i

if grundy_num == 0:
    print(0)
    exit(0)

answer = 0
for i in range(N):
    grundy_num = 0
    for j in range(N):
        if j == i:
            continue
        grundy_num ^= stones[j]
    for j in range(stones[i]):
        if grundy_num ^ j == 0:
            answer += 1
print(answer)