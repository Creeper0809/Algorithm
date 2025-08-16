import sys
input = sys.stdin.readline

t = int(input())
limits = [9,8,7,6,5,4,3,2,1,0]

for _ in range(t):
    digits = sorted(map(int, input().strip()))
    ans = []
    for lim in limits:
        for i, x in enumerate(digits):
            if x >= lim:
                ans.append(str(x))
                digits.pop(i)
                break
    print("".join(ans))
