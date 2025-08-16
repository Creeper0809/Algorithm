import math
from collections import deque

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def length(self):
        return math.hypot(self.x, self.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

def ccw(A, B, C):
    return (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)

def graham_scan(points):
    points.sort(key=lambda p: (p.y, p.x))
    base_point = points[0]
    points = [base_point] + sorted(points[1:], key=lambda p: math.atan2(p.y - base_point.y, p.x - base_point.x))
    stack = [points[0], points[1]]
    for p in points[2:]:
        while len(stack) >= 2 and ccw(stack[-2], stack[-1], p) <= 0:
            stack.pop()
        stack.append(p)
    return stack

def min_width(convex):
    n = len(convex)
    min_w = float('inf')
    for i in range(n):
        a = convex[i]
        b = convex[(i + 1) % n]
        edge = b - a
        normal = Point(-edge.y, edge.x)

        max_proj = -float('inf')
        min_proj = float('inf')
        for p in convex:
            vec = p - a
            proj = vec.dot(normal) / normal.length()
            max_proj = max(max_proj, proj)
            min_proj = min(min_proj, proj)

        min_w = min(min_w, max_proj - min_proj)
    return min_w

case_num = 1
while True:
    N = int(input())
    if N == 0:
        break

    points = [Point(*map(int, input().split())) for _ in range(N)]
    if N == 1:
        print(f"Case {case_num}: 0.00")
        case_num += 1
        continue

    convex = graham_scan(points)
    width = min_width(convex)
    width = math.ceil(width * 100) / 100
    print(f"Case {case_num}: {width:.2f}")
    case_num += 1
