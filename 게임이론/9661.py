import sys

sys.setrecursionlimit(10*7)

def calculate_grundy_dp(n, memo):
    # 돌이 0개일 때의 그런디 수는 0
    if n == 1:
        return 1
    # memoization
    if n in memo:
        return memo[n]
    s = set()
    for i in range(10):
        num = 4 ** i
        if n - num < 0:
            break
        s.add(calculate_grundy_dp(n - num, memo))

    grundy = 0
    # mex 함수를 계산하여 그런디 수를 결정
    while grundy in s:
        grundy += 1
    memo[n] = grundy
    return grundy

N = int(input())
if calculate_grundy_dp(N,{}) == 0:
    print("CY")
else:
    print("SK")