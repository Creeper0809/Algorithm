N = int(input())
temp = list(map(int, input().split()))

is_prime = [True] * 1001
is_prime[0] = is_prime[1] = False

for i in range(2, 1001):
    if not is_prime[i]:
        continue
    for j in range(i*i, 1001, i):
        is_prime[j] = False
answer = 0
for i in temp:
    if is_prime[i]:
        answer += 1
print(answer)