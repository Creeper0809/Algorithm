import sys
sys.setrecursionlimit(10 ** 7)
input = sys.stdin.readline

def divide_merge(pts):
    n = len(pts)
    if n <= 3:
        min_d = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                dx = pts[i][0] - pts[j][0]
                dy = pts[i][1] - pts[j][1]
                min_d = min(min_d, dx * dx + dy * dy)
        pts.sort(key=lambda p: p[1])
        return min_d, pts
    mid = n // 2
    mid_x = pts[mid][0]
    dl, left_sorted_by_y = divide_merge(pts[:mid])
    dr, right_sorted_by_y = divide_merge(pts[mid:])
    d = min(dl, dr)
    merged = []
    i = j = 0
    L, R = left_sorted_by_y, right_sorted_by_y
    while i < len(L) and j < len(R):
        if L[i][1] < R[j][1]:
            merged.append(L[i])
            i += 1
        else:
            merged.append(R[j])
            j += 1
    merged.extend(L[i:])
    merged.extend(R[j:])
    strip = [p for p in merged if (p[0] - mid_x) ** 2 < d]
    m = len(strip)
    for i in range(m):
        for j in range(i + 1, min(i + 7, m)):
            dx = strip[i][0] - strip[j][0]
            dy = strip[i][1] - strip[j][1]
            dist = dx * dx + dy * dy
            if dist < d:
                d = dist
    return d, merged

n = int(input())
points = [tuple(map(int, input().split())) for _ in range(n)]
points.sort()
distance, _ = divide_merge(points)
print(distance)
