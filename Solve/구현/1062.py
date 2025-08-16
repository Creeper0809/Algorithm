import itertools
import sys

N,K = map(int,input().split())
input = sys.stdin.readline
def solution():
    global K
    if K < 5:
        return 0
    answer = 0
    can_learn = []
    all_chars = set()
    for i in range(N):
        string_l = input().rstrip()
        alphabet_set = set(string_l)
        alphabet_len = len(alphabet_set)
        if alphabet_len == 5:
            answer += 1
        elif alphabet_len <= K:
            now_set = alphabet_set - {'a','n','t','i','c'}
            can_learn.append(now_set)
            all_chars |= now_set

    if len(can_learn) == 0:
        return answer

    if len(all_chars) <= K-5:
        return len(can_learn) + answer
    maxcount = 0
    for comb in itertools.combinations(all_chars, K-5):
        temp = 0
        for i in can_learn:
            if i.issubset(set(comb)):
                temp += 1
        maxcount = max(temp,maxcount)
    return answer + maxcount
print(solution())