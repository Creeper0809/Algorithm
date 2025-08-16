import sys
input = sys.stdin.readline


N = int(input())
result = N
i = 2
while i ** 2 <= N:
    if N % i == 0:
        result *= (1 - (1/i))
        while not N % i:
            N //= i
    i += 1

if N > 1:
    result *= 1 - 1 / N

print(round(result))