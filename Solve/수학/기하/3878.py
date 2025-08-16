import sys
input = sys.stdin.readline

class Point:
    __slots__ = ('x','y')
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __sub__(self, o):
        return Point(self.x - o.x, self.y - o.y)
    def dot(self, o):
        return self.x*o.x + self.y*o.y
    def cross(self, o):
        return self.x*o.y - self.y*o.x

def ccw(a, b, c):
    return (b - a).cross(c - a)

def convex_hull(pts):
    pts = sorted(pts, key=lambda p:(p.x,p.y))
    if len(pts) <= 1:
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
    return lower[:-1] + upper[:-1]

def on_segment(a, b, p):
    return (p - a).cross(b - a) == 0 and (p - a).dot(p - b) <= 0

def segments_intersect(a, b, c, d):
    o1, o2 = ccw(a,b,c), ccw(a,b,d)
    o3, o4 = ccw(c,d,a), ccw(c,d,b)
    if o1*o2 < 0 and o3*o4 < 0:
        return True
    if o1 == 0 and on_segment(a,b,c): return True
    if o2 == 0 and on_segment(a,b,d): return True
    if o3 == 0 and on_segment(c,d,a): return True
    if o4 == 0 and on_segment(c,d,b): return True
    return False

def point_in_convex(poly, p):
    n = len(poly)
    if n == 0:
        return False
    if n == 1:
        return p.x == poly[0].x and p.y == poly[0].y
    if n == 2:
        return on_segment(poly[0], poly[1], p)
    for i in range(n):
        if ccw(poly[i], poly[(i+1)%n], p) < 0:
            return False
    return True

t = int(input())
for _ in range(t):
    b, w = map(int, input().split())
    blacks = [Point(*map(int,input().split())) for _ in range(b)]
    whites = [Point(*map(int,input().split())) for _ in range(w)]
    hb = convex_hull(blacks)
    hw = convex_hull(whites)
    ok = True

    for i in range(len(hb)):
        for j in range(len(hw)):
            if segments_intersect(hb[i], hb[(i+1)%len(hb)], hw[j], hw[(j+1)%len(hw)]):
                ok = False
                break
        if not ok:
            break

    if ok:
        for p in blacks:
            if point_in_convex(hw, p):
                ok = False
                break

    if ok:
        for p in whites:
            if point_in_convex(hb, p):
                ok = False
                break

    print("YES" if ok else "NO")
