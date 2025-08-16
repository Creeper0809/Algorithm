n = int(input())
result = 1

for i in range(1,n + 1):
    result *= i
    while result % 10 == 0:
        result //= 10
    result %= int(1e15)

result_str = str(result).rstrip('0')
print(result_str[-5:].rjust(5,"0"))

