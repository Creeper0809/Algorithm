import sys
import math
import bisect

input = sys.stdin.readline

N = int(input().strip())
A = [0] + list(map(int, input().strip().split()))
block_size = math.ceil(math.sqrt(N))
num_blocks = math.ceil(N / block_size)
blocks = []
for i in range(num_blocks):
    start = i * block_size + 1
    end = min((i + 1) * block_size, N) + 1
    blocks.append(sorted(A[start:end]))

M = int(input().strip())
for _ in range(M):
    k,*args = list(map(int, input().strip().split()))
    if k == 1:
        i, j, k = args
        count = 0
        cur = i
        while cur <= j:
            bid = (cur - 1) // block_size
            bstart = bid * block_size + 1
            bend = min((bid + 1) * block_size, N)
            if cur == bstart and j >= bend:
                count += len(blocks[bid]) - bisect.bisect_right(blocks[bid], k)
                cur = bend + 1
            else:
                pend = min(j, bend)
                for p in range(cur, pend + 1):
                    if A[p] > k:
                        count += 1
                cur = pend + 1
        print(count)
    elif k == 2:
        idx, val = args
        old = A[idx]
        A[idx] = val
        bid = (idx - 1) // block_size
        pos = bisect.bisect_left(blocks[bid], old)
        if pos < len(blocks[bid]) and blocks[bid][pos] == old:
            del blocks[bid][pos]
        bisect.insort(blocks[bid], val)