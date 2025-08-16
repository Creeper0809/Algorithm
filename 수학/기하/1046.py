import sys
import math
from collections import defaultdict

def cross(ax, ay, bx, by):
    return ax * by - ay * bx

def dot(ax, ay, bx, by):
    return ax * bx + ay * by

def ray_hit_seg(Sx, Sy, dx, dy, Ax, Ay, Bx, By):
    rx, ry = dx, dy
    sx, sy = Bx - Ax, By - Ay
    qx, qy = Ax - Sx, Ay - Sy
    den = cross(rx, ry, sx, sy)

    # 평행 or 동일 선분
    if den == 0:
        if cross(qx, qy, rx, ry):  # 서로 다른 평행선
            return None
        # 동일 직선 → 끝점 두 개 중 앞쪽 끝만 고려
        rr = rx * rx + ry * ry
        tA = dot(qx, qy, rx, ry) / rr
        tB = dot(Bx - Sx, By - Sy, rx, ry) / rr
        cand = [t for t in (tA, tB) if t >= 0]
        return min(cand) if cand else None

    # 일반 교차
    t = cross(qx, qy, sx, sy) / den
    u = cross(qx, qy, rx, ry) / den
    return t if t >= 0 and 0 <= u <= 1 else None

def shoelace(area_pts):
    s = 0
    for i in range(len(area_pts)):
        x1, y1 = area_pts[i]
        x2, y2 = area_pts[(i + 1) % len(area_pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 8.0


N, M = map(int, sys.stdin.readline().split())
room = [sys.stdin.readline().strip() for _ in range(N)]

seg_list = []  # (x1,y1,x2,y2) 튜플
vertex_set = set()
Sx = Sy = -1  # 광원 좌표
wall_cnt = 0

for r in range(N):
    for c in range(M):
        ch = room[r][c]
        if ch == '*':  # 광원
            Sx, Sy = 2 * c + 1, 2 * r + 1
        if ch == '#':  # 벽(#)인 경우 네 변 추가
            wall_cnt += 1
            x, y = 2 * c, 2 * r
            seg_list += [
                (x, y, x + 2, y),
                (x + 2, y, x + 2, y + 2),
                (x + 2, y + 2, x, y + 2),
                (x, y + 2, x, y),
            ]
            vertex_set |= {(x, y), (x + 2, y), (x + 2, y + 2), (x, y + 2)}

# 방 테두리 4 변
seg_list += [
    (0, 0, 2 * M, 0),
    (2 * M, 0, 2 * M, 2 * N),
    (2 * M, 2 * N, 0, 2 * N),
    (0, 2 * N, 0, 0),
]
vertex_set |= {(0, 0), (2 * M, 0), (2 * M, 2 * N), (0, 2 * N)}

EPS = 1e-12
angle_list = []

for vx, vy in vertex_set:
    dx, dy = vx - Sx, vy - Sy
    theta = math.atan2(dy, dx)
    for d in (theta - EPS, theta, theta + EPS):
        if d < 0:
            d += 2 * math.pi
        if d >= 2 * math.pi:
            d -= 2 * math.pi
        angle_list.append(d)

angle_list = sorted(set(angle_list))  # 중복 제거 후 정렬
poly = []  # 시야 다각형 꼭짓점

for th in angle_list:
    dx, dy = math.cos(th), math.sin(th)
    best_t = None
    for Ax, Ay, Bx, By in seg_list:
        t_hit = ray_hit_seg(Sx, Sy, dx, dy, Ax, Ay, Bx, By)
        if t_hit is not None and (best_t is None or t_hit < best_t):
            best_t = t_hit
    if best_t is not None:
        px = Sx + best_t * dx
        py = Sy + best_t * dy
        # 직전 점과 거의 같으면 중복 제거
        if not poly or abs(px - poly[-1][0]) > EPS or abs(py - poly[-1][1]) > EPS:
            poly.append((px, py))

lit_area = 0.0
if len(poly) >= 3:
    lit_area = shoelace(poly)

total = N * M
shadow = total - lit_area - wall_cnt

print(f"{shadow}")
