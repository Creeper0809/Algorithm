import sys
import math

x0, x1 = -10.0, 10.0

EPS1 = 1e-7
XP1 = 1e-3

def _val_ypp1(y, yp, x):
    u = 2 * x * yp - 2 * y
    uu = x * x + y * y
    if uu < 1e-14: uu = 1e-14
    uu = uu * (uu + 1.0)
    lu = 1.0 + yp * yp
    return u * lu / uu


def trial1(s, a_rel):
    x = x0
    y = a_rel
    yp = s
    dose = 0.0

    while x < x1:
        seg = math.hypot(1.0, yp) * XP1
        dose += (1.0 + 1.0 / (x * x + y * y)) * seg

        x += XP1
        ypp = _val_ypp1(y, yp, x)
        y += yp * XP1
        yp += ypp * XP1

    return y, dose


def solve1(a, b, c0):
    a_rel = a - c0
    b_rel = b - c0

    lo, hi = -100.0, -a_rel / 10.0
    while abs(hi - lo) > EPS1:
        mid = 0.5 * (lo + hi)
        y_end, _ = trial1(mid, a_rel)
        if y_end < b_rel:
            lo = mid
        else:
            hi = mid
    down = trial1(0.5 * (lo + hi), a_rel)[1]

    lo, hi = -a_rel / 10.0, 100.0
    while abs(hi - lo) > EPS1:
        mid = 0.5 * (lo + hi)
        y_end, _ = trial1(mid, a_rel)
        if y_end < b_rel:
            lo = mid
        else:
            hi = mid
    up = trial1(0.5 * (lo + hi), a_rel)[1]

    return min(down, up)

EPS2 = 1e-7
XP2 = 5e-5


def trial2(s, a, c0, c1):
    x = x0
    y = a
    yp = s
    dose = 0.0

    while x < x1:
        inv0 = 1.0 / (x * x + (y - c0) ** 2)
        inv1 = 1.0 / (x * x + (y - c1) ** 2)
        seg = math.hypot(1.0, yp) * XP2
        dose += (1.0 + inv0 + inv1) * seg

        num = ((-2 * (y - c0) + 2 * x * yp) * inv0 * inv0
               + (-2 * (y - c1) + 2 * x * yp) * inv1 * inv1)

        den = 1.0 + inv0 + inv1
        ypp = (1.0 + yp * yp) * num / den

        x += XP2
        y += yp * XP2
        yp += ypp * XP2

    return y, dose


def solve2(a, b, c0, c1):
    if c0 > c1:
        c0, c1 = c1, c0

    lo, hi = -100.0, -((a - c0) / 10.0)
    while abs(hi - lo) > EPS2:
        mid = 0.5 * (lo + hi)
        y_end, _ = trial2(mid, a, c0, c1)
        if y_end < b:
            lo = mid
        else:
            hi = mid
    down = trial2(0.5 * (lo + hi), a, c0, c1)[1]

    lo, hi = -((a - c1) / 10.0), 100.0
    while abs(hi - lo) > EPS2:
        mid = 0.5 * (lo + hi)
        y_end, _ = trial2(mid, a, c0, c1)
        if y_end < b:
            lo = mid
        else:
            hi = mid
    up = trial2(0.5 * (lo + hi), a, c0, c1)[1]

    lo, hi = -((a - c0) / 10.0), -((a - c1) / 10.0)
    while abs(hi - lo) > EPS2:
        mid = 0.5 * (lo + hi)
        y_end, _ = trial2(mid, a, c0, c1)
        if y_end < b:
            lo = mid
        else:
            hi = mid
    mid_d = trial2(0.5 * (lo + hi), a, c0, c1)[1]

    return min(down, up, mid_d)


def main():
    input = sys.stdin.readline
    T = int(input())
    for tc in range(1, T + 1):
        data = list(map(float, input().split()))
        n = int(data[0])
        a, b = data[1], data[2]

        if n == 1:
            c0 = float(input())
            ans = solve1(a, b, c0)
        else:
            c0, c1 = map(float, input().split())
            ans = solve2(a, b, c0, c1)

        print(f"Case #{tc}: {ans:.2f}")

if __name__ == "__main__":
    main()
