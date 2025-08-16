N = int(input())

for i in range(N-1):
    temp = i
    temp2 = i
    while temp > 0:
        temp2 += temp%10
        temp //= 10
    if temp2 == N:
        print(i)
        exit(0)
print(0)