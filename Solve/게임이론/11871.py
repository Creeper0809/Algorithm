N = int(input())
stones = list(map(int, input().split()))
grundy_num = 0
for i in stones:
    if i % 2 == 0:
        grundy_num ^= i // 2 - 1
    else:
        grundy_num ^= i // 2 + 1

if grundy_num == 0:
    print("cubelover")
else:
    print("koosaga")
