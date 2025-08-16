import sys
from collections import defaultdict
from math import sqrt
input = sys.stdin.readline

N = int(input())
arr = list(map(int, input().split()))
M = int(input())
queries = []

for i in range(M):
    l,r = map(int, input().split())
    queries.append((l-1,r-1,i))

def mos(arr,queries):
    n = len(arr)
    block_size = int(sqrt(n))
    queries = sorted(queries, key=lambda x: (x[0] // block_size, x[1]))

    result = [0] * len(queries)
    freq = defaultdict(int)
    max_freq = 0

    currL, currR = 0, -1

    for L,R,idx in queries:
        while currL > L:
            currL -= 1
            freq[arr[currL]] += 1
            if freq[arr[currL]] == 1:
                max_freq += 1
        while currR < R:
            currR += 1
            freq[arr[currR]] += 1
            if freq[arr[currR]] == 1:
                max_freq += 1
        while currL < L:
            freq[arr[currL]] -= 1
            if freq[arr[currL]] == 0:
                max_freq -= 1
            currL += 1

        while currR > R:
            freq[arr[currR]] -= 1
            if freq[arr[currR]] == 0:
                max_freq -= 1
            currR -= 1


        result[idx] = max_freq
    return result

result = mos(arr, queries)

for i in result:
    print(i)


