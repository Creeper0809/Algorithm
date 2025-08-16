import sys
input = sys.stdin.readline

M = int(input())
heaps = list(map(int, input().split()))
max_h = max(heaps)

fibs = [1, 2]
while fibs[-1] + fibs[-2] <= max_h:
    fibs.append(fibs[-1] + fibs[-2])

sg = [0] * (max_h + 1)
for i in range(1, max_h + 1):
    seen = set()
    for f in fibs:
        if f > i:
            break
        seen.add(sg[i - f])
    m = 0
    while m in seen:
        m += 1
    sg[i] = m

res = 0
for h in heaps:
    res ^= sg[h]

if res == 0:
    print("cubelover")
else:
    print("koosaga")
