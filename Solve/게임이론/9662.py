import sys

input = sys.stdin.readline
M = int(input().rstrip())
K = int(input().rstrip())
moves = list(map(int,input().split()))

NNN = 300000
NN = 100000
dp = [0] * (NNN+1)
m = 0
for i in range(1,NNN+1):
    for move in moves:
        state = i - move
        if state < 0:
            break
        m |= (1<<dp[state])
    grundy = 0
    while m > 0:
        if m & 1 == 0:
            break
        grundy += 1
        m >>= 1
    dp[i] = grundy
    m = 0
answer = 0
if M < NN:
    for i in range(1,M+1):
        if dp[i] == 0:
            answer+=1
    print(answer)
else:
    for i in range(1,NN+1):
        if dp[i] == 0:
            answer+=1
    length = 1
    for i in range(2,2000):
        is_cycle = True
        for j in range(NN+1,NN + 2001):
            if dp[j] != dp[j + i]:
                is_cycle = False
                break
        if is_cycle:
            length = max(length,i)
    count = 0
    for i in range(NN+1,NN+1+length):
        if dp[i] == 0:
            count+=1
    answer += ((M-NN)//length) * count
    for i in range(NN+1,(NN + ((M-NN)%length))+1):
        if dp[i] == 0:
            answer+=1
    print(answer)
