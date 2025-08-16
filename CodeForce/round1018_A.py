import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()

    k = s.count('<')
    ans = [0] * n
    ans[0] = k + 1

    small = k
    large = k + 2

    for i, ch in enumerate(s, start=1):
        if ch == '<':
            ans[i] = small
            small -= 1
        else:
            ans[i] = large
            large += 1

    print(*ans)
