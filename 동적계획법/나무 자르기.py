import sys

input = sys.stdin.readline

MAX = 100000

class LinearFunc:
    def __init__(self, a=1, b=0, s=0):
        self.a = a  # 기울기
        self.b = b  # 절편
        self.s = s  # 시작하는 x좌표 (유효구간 시작점)

def cross(f, g):
    return (g.g - f.g) / (f.arr - g.arr)

def main():
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    dp = [0] * N
    f = []
    top = 0

    for i in range(1, N):
        g = LinearFunc(B[i-1], dp[i-1])

        while top > 0:
            g.s = cross(f[top-1], g)
            if f[top-1].s < g.s:
                break
            top -= 1
            f.pop()

        f.append(g)
        top = len(f)

        x = A[i]
        fpos = top - 1
        if x < f[top-1].s:
            lo, hi = 0, top - 1
            while lo + 1 < hi:
                mid = (lo + hi) // 2
                if x < f[mid].s:
                    hi = mid
                else:
                    lo = mid
            fpos = lo

        dp[i] = f[fpos].f * x + f[fpos].g

    print(dp[N-1])

if __name__ == "__main__":
    main()
