import sys
import math


def compute_time_via_layers(w, segments, v_h):
    if not segments:
        return v_h * w

    def F(C):
        return sum(dy * C / math.sqrt(v * v - C * C) for dy, v in segments)

    v_min = min(v for _, v in segments)
    if all(v > v_h for _, v in segments) and F(v_h) <= w:
        C = v_h
    else:
        L, R = 0.0, v_min - 1e-12
        for _ in range(100):
            C = 0.5 * (L + R)
            if F(C) > w:
                R = C
            else:
                L = C
        C = 0.5 * (L + R)

    dx_diag = F(C)
    dx_hor = w - dx_diag
    T_diag = sum(v * v * dy / math.sqrt(v * v - C * C) for dy, v in segments)
    T_hor = v_h * dx_hor
    return T_diag + T_hor


def main():
    input = sys.stdin.readline
    w, _ = map(int, input().split())
    n, d = map(int, input().split())
    a_list = list(map(int, input().split()))
    p = list(map(float, input().split()))

    A = [0.0] + a_list
    y0, y1 = 0.0, float(d)

    s = e = -1
    for i in range(n):
        top = A[i]
        bottom = A[i + 1] if i + 1 < n else float('inf')
        if top <= y0 <= bottom:
            s = i
        if top <= y1 <= bottom:
            e = i

    k = n - 1
    best = float('inf')
    if s == e:
        best = p[s] * math.hypot(w, y1 - y0)

    for m in range(max(s, e), k + 1):
        segments = []
        curr_y = y0

        for i in range(s, m):
            dest_y = A[i + 1]
            segments.append((dest_y - curr_y, p[i]))
            curr_y = dest_y

        for i in range(m - 1, e, -1):
            dest_y = A[i]
            segments.append((curr_y - dest_y, p[i]))
            curr_y = dest_y

        segments.append((abs(y1 - curr_y), p[e]))
        print(segments)
        candidate = compute_time_via_layers(w, segments, p[m])
        best = min(best, candidate)

    print(f"{best:.6f}")


if __name__ == "__main__":
    main()
