import operator
import sys
from functools import reduce


sys.setrecursionlimit(10 ** 5)

def mobius_values(n):
    global mobius
    mobius = [0] * n
    mobius[1] = 1
    for i in range(1, n):
        if mobius[i]:
            for j in range(i * 2, n, i):
                mobius[j] -= mobius[i]

def square_free_num_no(n):
    no = n
    for i in range(2,int(n**0.5)+1):
        no += mobius[i] * (n//(i*i))
    return no


k = int(input())

high = 200000000000
low = 0
mobius_values(1000001)
while high-1 > low:
    mid = (low + high) // 2
    if mid - square_free_num_no(mid)>=k:
        high = mid
    else:
        low = mid
print(high)
