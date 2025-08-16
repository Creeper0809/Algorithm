N,M = map(int,input().split())
primes = [True] * (M+1)
primes[0] = primes[1] = False
for i in range(2,int(M**0.5)+1):
    if not primes[i]:
        continue
    for j in range(i*i,M+1,i):
        primes[j] = False

for i in range(N,M+1):
    if primes[i]:
        print(i)
