import sys
input = sys.stdin.readline

def popcnt(x):
    return x.bit_count()

def f2(T):
    if T == 0:
        return 2
    if T == 1:
        return 5
    # popcount >= 2
    if popcnt(T) >= 2:
        return T
    # popcount == 1, T>1
    return T + 2

def solve_one(n, x):
    if n == 1:
        return -1 if x == 0 else x

    # n >= 2
    if x == (n & 1):
        return n
    T = x ^ ((n - 2) & 1)
    return (n - 2) + f2(T)

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        n, x = map(int, input().split())
        ans.append(str(solve_one(n, x)))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
