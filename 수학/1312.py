A,B,N = map(int,input().split())

answer = 0

for i in range(N+1):
    answer = A//B
    A %= B
    A *= 10
print(answer)
