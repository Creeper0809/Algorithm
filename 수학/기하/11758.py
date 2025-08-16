class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def ccw(A: Point, B: Point, C: Point) -> int:
    result = (B.x - A.x) * (C.y - A.y) - (C.x - A.x) * (B.y - A.y)

    if result > 0:
        return 1  # 반시계 방향
    elif result < 0:
        return -1  # 시계 방향
    else:
        return 0  # 일직선


x,y = map(int,input().split())
A = Point(x,y)
x,y = map(int,input().split())
B = Point(x,y)
x,y = map(int,input().split())
C = Point(x,y)
print(ccw(A,B,C))