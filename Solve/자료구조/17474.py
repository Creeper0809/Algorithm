import sys

input = sys.stdin.readline
sys.setrecursionlimit(10 ** 5)

N = int(input())
arr = list(map(int, input().split()))

INF = 1 << 60
size = 4 * N
mx = [0] * size
se = [0] * size
cnt = [0] * size
sum_ = [0] * size
lazy = [INF] * size


def build_node(idx):
    L = idx << 1
    R = L | 1
    sum_[idx] = sum_[L] + sum_[R]
    if mx[L] > mx[R]:
        mx[idx], cnt[idx] = mx[L], cnt[L]
        se[idx] = max(se[L], mx[R])
    elif mx[L] < mx[R]:
        mx[idx], cnt[idx] = mx[R], cnt[R]
        se[idx] = max(mx[L], se[R])
    else:
        mx[idx] = mx[L]
        cnt[idx] = cnt[L] + cnt[R]
        se[idx] = max(se[L], se[R])


def apply(idx, x):
    sum_[idx] -= (mx[idx] - x) * cnt[idx]
    mx[idx] = x
    lazy[idx] = x

def build_tree(idx, l, r):
    if l == r:
        v = arr[l]
        mx[idx] = v
        se[idx] = -INF
        cnt[idx] = 1
        sum_[idx] = v
        lazy[idx] = INF
        return
    m = (l + r) >> 1
    build_tree(idx << 1, l, m)
    build_tree((idx << 1) | 1, m + 1, r)
    build_node(idx)

def push_down(idx, l, r):
    if l == r:
        return
    if lazy[idx] == INF:
        return
    for c in (idx << 1, (idx << 1) | 1):
        if mx[c] > mx[idx]:
            sum_[c] -= (mx[c] - mx[idx]) * cnt[c]
            mx[c] = mx[idx]
            lazy[c] = mx[idx]
    lazy[idx] = INF

def range_update(idx, l, r, L, R, x):
    if r < L or R < l or mx[idx] <= x:
        return
    if L <= l and r <= R and se[idx] < x:
        apply(idx, x)
        return
    push_down(idx, l, r)
    m = (l + r) >> 1
    range_update(idx << 1, l, m, L, R, x)
    range_update((idx << 1) | 1, m + 1, r, L, R, x)
    build_node(idx)


def range_query_max(idx, l, r, L, R):
    if r < L or R < l:
        return -INF
    if L <= l and r <= R:
        return mx[idx]
    push_down(idx,l,r)
    m = (l + r) >> 1
    return max(
        range_query_max(idx << 1, l, m, L, R),
        range_query_max((idx << 1) | 1, m + 1, r, L, R)
    )


def range_query_sum(idx, l, r, L, R):
    if r < L or R < l:
        return 0
    if L <= l and r <= R:
        return sum_[idx]
    push_down(idx,l,r)
    m = (l + r) >> 1
    return (
            range_query_sum(idx << 1, l, m, L, R) +
            range_query_sum((idx << 1) | 1, m + 1, r, L, R)
    )


M = int(input())
build_tree(1, 0, N - 1)
out = []
append_out = out.append
for _ in range(M):
    q = list(map(int, input().split()))
    t, L, R = q[0], q[1] - 1, q[2] - 1
    if t == 1:
        range_update(1, 0, N - 1, L, R, q[3])
    elif t == 2:
        append_out(str(range_query_max(1, 0, N - 1, L, R)))
    else:
        append_out(str(range_query_sum(1, 0, N - 1, L, R)))

sys.stdout.write("\n".join(out) + "\n")
