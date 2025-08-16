import sys
input = sys.stdin.readline

def count_palindromes(s):
    T = ['^']
    for ch in s:
        T += ['#', ch]
    T += ['#', '$']
    N = len(T)
    P = [0] * N
    center = right = 0
    for i in range(1, N - 1):
        mirror = 2*center - i
        if i < right:
            P[i] = min(right - i, P[mirror])
        while T[i + (1 + P[i])] == T[i - (1 + P[i])]:
            P[i] += 1
        if i + P[i] > right:
            center, right = i, i + P[i]
    return sum(p // 2 for p in P)

s = input().rstrip()
print(count_palindromes(s) + len(s))
