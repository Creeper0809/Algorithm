n = int(input())

sieve = [True] * (n+1)  # 모든 수를 소수로 간주

for i in range(2, int(n**0.5)+1):
    if sieve[i]:
        for j in range(i*2, n+1, i):
            sieve[j] = False  # i의 배수 제거

primes = []
prime_cnt = 0
# 소수 출력
for i in range(2, n+1):
    if sieve[i]:
        primes.append(i)
        prime_cnt += 1

left,right = 0,0
answer = 0
while right<=prime_cnt:
    prime_sum = sum(primes[left:right])
    if prime_sum == n:
        answer += 1
        right += 1
    elif prime_sum < n:
        right+=1
    else:
        left+=1
print(answer)