import sys

input = sys.stdin.readline
n = int(input())
T = list(map(int, input().split()))

R = T[::-1]

kmp = [0] * n
j = 0
for i in range(1, n):
    while j > 0 and R[i] != R[j]:
        j = kmp[j - 1]
    if R[i] == R[j]:
        j += 1
    kmp[i] = j

max_pi = -1
best_i = 0
for i, v in enumerate(kmp):
    if v > max_pi:
        max_pi = v
        best_i = i

L = best_i + 1
p = L - max_pi
k = n - L

print(k, p)
