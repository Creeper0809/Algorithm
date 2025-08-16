import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

p = (3 << 18) | 1
g = 10

def Add(a, b):
    s = a + b
    return s if s < p else s - p

def Sub(a, b):
    return a - b if a >= b else a - b + p

def Mul(a, b):
    return (a * b) % p

def FFT(f, w):
    n = len(f)
    if n == 3:
        a, b, c = f[0], f[1], f[2]
        f[0] = (a + b + c) % p
        f[1] = (a + b*w + ((c*w) % p)*w) % p
        w = (w * w) % p
        f[2] = (a + b*w + ((c*w) % p)*w) % p
    else:
        A = f[0::2]
        B = f[1::2]
        FFT(A, Mul(w, w))
        FFT(B, Mul(w, w))
        x = 1
        for i in range(n // 2):
            f[i] = Add(A[i], Mul(x, B[i]))
            f[i + n//2] = Sub(A[i], Mul(x, B[i]))
            x = Mul(x, w)

def main():
    n = int(input())
    coeffs = list(map(int, input().split()))
    N = 3 << 18
    f = [0] * N
    for i in range(n + 1):
        f[i] = coeffs[i]

    I = [0] * p
    x = 1
    for k in range(N):
        I[x] = k
        x = Mul(x, g)

    f0 = f[0]
    FFT(f, g)

    q = int(input())
    query = list(map(int,input().split()))
    out = []
    for x in query:
        if x == 0:
            out.append(str(f0))
        else:
            out.append(str(f[I[x]]))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
