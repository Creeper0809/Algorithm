n,m = map(int,input().split())  # 찾고자 하는 범위
sieve = [True] * (n+1)  # 모든 수를 소수로 간주
count = 1

for i in range(2,n+1):
    if sieve[i]:
        for j in range(i,n+1,i):
            if not sieve[j]:
                continue
            sieve[j] = False
            if count == m:
                print(j)
                exit(0)
            count+=1