import sys
from collections import Counter

input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    cnt = Counter(a)

    # 1) 한 날에 4번 이상 베팅 있으면 무조건 Yes
    if any(c >= 4 for c in cnt.values()):
        print("Yes")
        continue

    # 2) 연속하는 베팅일 구간마다, 베팅 횟수 >=2인 날이 두 번 이상 있으면 Yes
    days = sorted(cnt.keys())
    prev = None
    run_two = 0
    ok = False
    for d in days:
        if prev is None or d != prev + 1:
            run_two = 0
        if cnt[d] >= 2:
            run_two += 1
            if run_two >= 2:
                ok = True
                break
        prev = d

    print("Yes" if ok else "No")
