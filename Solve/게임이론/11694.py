N = int(input())
grundy_num = 0
stones = list(map(int,input().split()))
one = 0
flag = True
for i in stones:
    if i == 1:
        one += 1
    else:
        flag = False
    grundy_num ^= i


if flag:
    print("koosaga") if one % 2 == 0 else print("cubelover")
    exit(0)

if one % 2 == 0:
    if grundy_num != 0:
        print("cubelover")
    else:
        print("koosaga")
else:
    if grundy_num == 0:
        print("cubelover")
    else:
        print("koosaga")
