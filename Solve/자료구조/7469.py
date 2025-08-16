import sys, bisect

input = sys.stdin.readline
sys.setrecursionlimit(10 ** 7)

N, M = map(int, input().split())
arr = list(map(int, input().split()))
tree = [[] for _ in range(4 * N)]


def merge(a, b):
    i = j = 0
    la, lb = len(a), len(b)
    merged = []
    while i < la and j < lb:
        if a[i] < b[j]:
            merged.append(a[i]);
            i += 1
        else:
            merged.append(b[j]);
            j += 1
    if i < la: merged.extend(a[i:])
    if j < lb: merged.extend(b[j:])
    return merged


def build(node, start, end):
    if start == end:
        tree[node] = [arr[start]]
    else:

        mid = (start + end) // 2
        build(node * 2, start, mid)
        build(node * 2 + 1, mid + 1, end)
        tree[node] = merge(tree[node * 2], tree[node * 2 + 1])


def count_leq(node, start, end, L, R, x):
    if R < start or end < L:
        return 0
    if L <= start and end <= R:
        return bisect.bisect_right(tree[node], x)
    mid = (start + end) // 2
    return (count_leq(node * 2, start, mid, L, R, x)
            + count_leq(node * 2 + 1, mid + 1, end, L, R, x))


def kth_smallest(l, r, k):
    lo, hi = 0, len(values) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if count_leq(1, 0, N - 1, l, r, values[mid]) >= k:
            hi = mid
        else:
            lo = mid + 1
    return values[lo]


build(1, 0, N - 1)

values = sorted(set(arr))

for _ in range(M):
    l, r, k = map(int, input().split())
    print(kth_smallest(l - 1, r - 1, k))
