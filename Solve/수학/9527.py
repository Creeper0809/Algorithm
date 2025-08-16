A,B = map(int,input().split())
# dp = [-1] * (B+1)
#
# total_count = 0
# for i in range(A,B+1):
#     cnt = 0
#     num = i
#     while num > 0:
#         num &= num - 1
#         cnt += 1
#         if dp[num] != -1:
#             cnt += dp[num]
#             break
#     dp[i] = cnt
#     total_count += cnt
#
# print(total_count)

dp = [0 for i in range(60)]
for i in range(1,60):
    dp[i] = 2**(i-1) + 2*dp[i-1]

def get_sum(num):
    count = 0
    bin_num = bin(num)[2:]
    length = len(bin_num)
    for i in range(length):
        if bin_num[i] == "1":
            beneth_pow = length - i -1
            count += dp[beneth_pow]
            count += (num-2 ** beneth_pow + 1)
            num = num -2 **beneth_pow
    return count


print(get_sum(B) - get_sum(A-1))


