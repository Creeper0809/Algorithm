import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    L = list(map(int, input().split()))
    R = list(map(int, input().split()))

    S_max = 0
    mins = []
    for l, r in zip(L, R):
        S_max += max(l, r)
        mins.append(min(l, r))

    mins.sort(reverse=True)
    extra = sum(mins[:k-1]) if k-1 > 0 else 0

    answer = S_max + extra + 1
    print(answer)
