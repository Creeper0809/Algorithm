import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()

    initial_move = 1 if s[0] == '1' else 0
    trans_cnt = sum(1 for i in range(1, n) if s[i] != s[i-1])
    cost0 = n + initial_move + trans_cnt

    best_gain = 0

    pos01 = [i for i in range(1, n) if s[i-1]=='0' and s[i]=='1']
    pos10 = [i for i in range(1, n) if s[i-1]=='1' and s[i]=='0']
    if len(pos01) >= 2 and pos01[-1] - pos01[0] >= 2:
        best_gain = 2
    elif len(pos10) >= 2 and pos10[-1] - pos10[0] >= 2:
        best_gain = 2

    elif s[0] == '1' and any(i >= 2 for i in pos01):
        best_gain = 2

    if best_gain < 2:

        for i in range(1, n-1):
            if s[i-1] != s[i] and s[i-1] == s[-1]:
                best_gain = 1
                break

    if best_gain < 2:
        for r in range(1, n-1):
            old_i = initial_move
            t_r   = 1 if s[r] != s[r+1] else 0
            new_i = 1 if s[r] == '1' else 0
            new_t = 1 if s[0] != s[r+1] else 0
            gain = old_i + t_r - new_i - new_t
            if gain > best_gain:
                best_gain = gain
                if best_gain == 1:
                    break

    if best_gain < 1 and s[0] == '1' and s[-1] == '0':
        best_gain = 1

    print(cost0 - best_gain)
