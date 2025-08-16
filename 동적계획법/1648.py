import sys

sys.setrecursionlimit(10**6)

input = sys.stdin.readline
N, M = map(int, input().split())
rows, cols = min(N, M), max(N, M)
MAX_MASK = 1 << rows

from collections import Counter

trans = [None] * MAX_MASK


def build_transitions(start_mask):
    cnt = Counter()

    def dfs(pos, cur_mask, next_mask):
        if pos == rows:
            cnt[next_mask] += 1
            return
        if cur_mask & (1 << pos):
            dfs(pos + 1, cur_mask, next_mask)
        else:
            if pos + 1 < rows and not (cur_mask & (1 << (pos + 1))):
                dfs(pos + 2, cur_mask, next_mask)
            dfs(pos + 1, cur_mask, next_mask | (1 << pos))

    dfs(0, start_mask, 0)
    return list(cnt.items())


for mask in range(MAX_MASK):
    trans[mask] = build_transitions(mask)

dp = {0: 1}
for _ in range(cols):
    nxt = {}
    for mask, ways in dp.items():
        for nm, cnt in trans[mask]:
            nxt[nm] = nxt.get(nm, 0) + ways * cnt
    dp = nxt
print(dp.get(0, 0) % 9901)
