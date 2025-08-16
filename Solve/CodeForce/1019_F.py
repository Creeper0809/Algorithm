import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        mask = (1 << k) - 1

        # next_nonmask: a[j] != mask(모두 1)인 첫 위치
        next_nonmask = [n] * (n + 1)
        for i in range(n - 1, -1, -1):
            next_nonmask[i] = i if a[i] != mask else next_nonmask[i + 1]

        ans = [0] * n
        prev = []

        for i in range(n):
            # 왼쪽 누적 NOR 상태(cur)
            cur = [a[i]]
            last = a[i]
            for v in prev:
                nv = mask & ~(v | a[i])
                if nv != last:
                    cur.append(nv)
                    last = nv

            best = 0
            # 각 시작 상태 vL에 대해 오른쪽 이벤트 스윕
            for vL in cur:
                if vL > best:
                    best = vL

                cur_v = vL
                idx = i + 1
                while idx < n:
                    # v != 0인 경우엔 반드시 idx에서 변화
                    if cur_v != 0:
                        nxt = idx
                    # v == 0인 경우엔 a[j]가 모두 1(mask)이면 변화 없으므로 건너뛰기
                    else:
                        nxt = next_nonmask[idx]

                    if nxt >= n:
                        break
                    # 한 번 NOR 누적
                    cur_v = mask & ~(cur_v | a[nxt])
                    if cur_v > best:
                        best = cur_v
                    idx = nxt + 1

            ans[i] = best
            prev = cur

        print(*ans)

if __name__ == "__main__":
    solve()
