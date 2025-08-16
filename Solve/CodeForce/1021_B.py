import sys
input=sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    m = n - k
    if m % 2 == 1:
        # m=2p+1
        p = (m - 1) // 2
        L = a[p]
        R = a[n - 1 - p]
    else:
        # m=2p
        p = m // 2
        L = a[p - 1]
        R = a[n - p]

    # 가능한 x의 구간이 [L, R] 하나로 이어지므로
    print(R - L + 1)
