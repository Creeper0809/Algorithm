import sys
input = sys.stdin.readline

MOD = 10**9+7
N = int(input())
nums = list(map(int, input().split()))
K = 10  # depth 최대값

# bit[d][i] 는 depth=d 에서 위치 i 의 Fenwick Tree
bit = [[0]*(N+1) for _ in range(K+1)]

def add(b, i, v):
    while i <= N:
        b[i] = (b[i] + v) % MOD
        i += i & -i

def query(b, i):
    s = 0
    while i > 0:
        s = (s + b[i]) % MOD
        i -= i & -i
    return s

for x in nums:
    # depth = 0 에서 1 추가
    add(bit[0], x, 1)
    if x > 1:
        # depth = j 에서 dp[x] = sum_{d=j-1}[1..x-1]
        for j in range(1, K+1):
            cnt = query(bit[j-1], x-1)
            add(bit[j], x, cnt)

# 전체 depth=K 의 합
print(query(bit[K], N))
