import sys
import math
input = sys.stdin.readline

def solve(x,y,x2,y2):
    if x > x2:
        x, x2 = x2, x
    if y > y2:
        y, y2 = y2, y

    if x == x2:
        return math.log(y2) - math.log(y)

    tau = math.atan((y2 - y) / (x2 - x))

    x3 = (x + x2) / 2
    y3 = (y + y2) / 2

    x4 = y3 * math.tan(tau) + x3

    theta1 = math.atan2(y, x4 - x)
    theta2 = math.atan2(y2, x4 - x2)

    val1 = math.log(abs(math.tan(theta1 / 2)))
    val2 = math.log(abs(math.tan(theta2 / 2)))

    return abs(val2 - val1)


def main():
    t = int(input())
    for _ in range(t):
        x, y, x2, y2 = map(float, sys.stdin.readline().split())
        sys.stdout.write(f"{solve(x, y, x2, y2):.6f}\n")

if __name__ == "__main__":
    main()