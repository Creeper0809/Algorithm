import sys
input = sys.stdin.readline

def ccw(a, b, c):
    return (a[0] * (b[1] - c[1])
          + b[0] * (c[1] - a[1])
          + c[0] * (a[1] - b[1]))

def convex_hull(points):
    pts = sorted(points)
    n = len(pts)
    if n <= 1:
        return pts[:]
    lower = []
    for p in pts:
        while len(lower) >= 2 and ccw(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and ccw(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    lower.pop()
    upper.pop()
    hull = lower + upper
    return hull

def dist2(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy

def farthest_pair(hull):
    m = len(hull)
    if m <= 1:
        if m == 1:
            return hull[0], hull[0]
        return None, None
    j = 1
    best_i = 0
    best_j = 1
    best_d = dist2(hull[0], hull[1])
    for i in range(m):
        ni = i + 1
        if ni == m:
            ni = 0
        while True:
            nj = j + 1
            if nj == m:
                nj = 0
            if ccw(hull[i], hull[ni], hull[nj]) > ccw(hull[i], hull[ni], hull[j]):
                j = nj
            else:
                break
        d = dist2(hull[i], hull[j])
        if d > best_d:
            best_d = d
            best_i = i
            best_j = j
    return hull[best_i], hull[best_j]


T = int(input())
for _ in range(T):
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    hull = convex_hull(pts)
    p, q = farthest_pair(hull)
    if p is None:
        sys.stdout.write("\n")
    else:
        sys.stdout.write(f"{p[0]} {p[1]} {q[0]} {q[1]}\n")

