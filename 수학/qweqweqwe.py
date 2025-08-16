import math
import sys

EPS = 1e-12          # 이분 탐색 오차 한계

def solve_case(x1, y1, x2, y2):
    if x1 == x2:                       # 순수 수직
        return abs(math.log(y2 / y1))
    if y1 == y2:                       # 순수 수평
        return abs(x2 - x1) / y1

    # 항상 x2 > x1 로 정렬
    if x2 < x1:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    dx = x2 - x1

    # 이분 탐색으로 C 찾아-내기
    ymax = max(y1, y2)
    lo, hi = 0.0, 1.0 / ymax - EPS

    def f(C):
        return (math.sqrt(1 - (C * y1) ** 2) -
                math.sqrt(1 - (C * y2) ** 2)) / C - dx

    while hi - lo > 1e-12:
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    C = (lo + hi) / 2

    # 최단 시간 (식 2)
    T = math.atanh(C * y2) - math.atanh(C * y1)
    return T

def main() -> None:
    it = map(int, sys.stdin.read().split())
    T = next(it)
    out_lines = []
    for _ in range(T):
        x1, y1, x2, y2 = (next(it), next(it), next(it), next(it))
        out_lines.append(f"{solve_case(x1, y1, x2, y2):.6f}")
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
