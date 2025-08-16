import sys

N = int(input())
num = list(map(int, input().split()))
op = list(map(int, input().split()))

min_op = sys.maxsize
max_op = -1000000000000
def operator(a,b):
    return [a+b, a-b, a*b, div(a,b)]

def div(a, b):
    if a < 0:
        return -(-a // b)
    return a // b

def dfs(numbers,now):
    global min_op,max_op,op
    if not numbers:
        min_op = min(min_op,now)
        max_op = max(max_op,now)
        return
    temp = operator(now,numbers[0])
    for i in range(4):
        if op[i] > 0:
            op[i] -= 1
            dfs(numbers[1:],temp[i])
            op[i] += 1

dfs(num[1:],num[0])

print(max_op)
print(min_op)