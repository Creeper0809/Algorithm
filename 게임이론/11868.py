N = int(input())
grundy_num = 0
stones = list(map(int,input().split()))
for i in stones:
    grundy_num ^= i
if grundy_num == 0:
    print("cubelover")
else:
    print("koosaga")