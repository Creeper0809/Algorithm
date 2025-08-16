import sys

input = sys.stdin.readline

INF = float('inf')
NINF = float('-inf')

class Node:
    def __init__(self, prefix=0, suffix=0, sub=0, total=0):
        self.prefix = prefix
        self.suffix = suffix
        self.sub = sub
        self.total = total

class SegTree:
    def __init__(self, arr):
        self.n = len(arr) - 1
        self.tree = [Node() for _ in range(4 * (self.n + 1))]
        self.build(1, 1, self.n, arr)

    def build(self, node, start, end, arr):
        if start == end:
            val = arr[start]
            self.tree[node] = Node(val, val, val, val)
            return
        mid = (start + end) // 2
        self.build(2 * node, start, mid, arr)
        self.build(2 * node + 1, mid + 1, end, arr)
        self.tree[node] = self.merge(self.tree[2 * node], self.tree[2 * node + 1])

    def merge(self, left, right):
        prefix = max(left.prefix, left.total + right.prefix)
        suffix = max(right.suffix, right.total + left.suffix)
        sub = max(left.sub, right.sub, left.suffix + right.prefix)
        total = left.total + right.total
        return Node(prefix, suffix, sub, total)

    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return None
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_q = self.query(2 * node, start, mid, l, r)
        right_q = self.query(2 * node + 1, mid + 1, end, l, r)
        if left_q is None:
            return right_q
        if right_q is None:
            return left_q
        return self.merge(left_q, right_q)

class MinSeg:
    def __init__(self, arr):
        self.n = len(arr) - 1
        self.tree = [INF] * (4 * (self.n + 1))
        self.build(1, 0, self.n, arr)

    def build(self, node, start, end, arr):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self.build(2 * node, start, mid, arr)
        self.build(2 * node + 1, mid + 1, end, arr)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return INF
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return min(self.query(2 * node, start, mid, l, r), self.query(2 * node + 1, mid + 1, end, l, r))

class MaxSeg:
    def __init__(self, arr):
        self.n = len(arr) - 1
        self.tree = [NINF] * (4 * (self.n + 1))
        self.build(1, 0, self.n, arr)

    def build(self, node, start, end, arr):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self.build(2 * node, start, mid, arr)
        self.build(2 * node + 1, mid + 1, end, arr)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return NINF
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return max(self.query(2 * node, start, mid, l, r), self.query(2 * node + 1, mid + 1, end, l, r))

N = int(input())
A = [0] + list(map(int, input().split()))
P = [0] * (N + 1)
for i in range(1, N + 1):
    P[i] = P[i - 1] + A[i]

seg = SegTree(A)
minp = MinSeg(P)
maxp = MaxSeg(P)

M = int(input())
for _ in range(M):
    x1, y1, x2, y2 = map(int, input().split())
    if y1 < x2:
        max_suf = seg.query(1, 1, N, x1, y1).suffix if x1 <= y1 else NINF
        tot_mid = P[x2 - 1] - P[y1]
        max_pre = seg.query(1, 1, N, x2, y2).prefix if x2 <= y2 else NINF
        ans = max_suf + tot_mid + max_pre
    else:
        ans = seg.query(1, 1, N, x2, y1).sub if x2 <= y1 else NINF
        if x1 < x2:
            min_left = minp.query(1, 0, N, x1 - 1, x2 - 2)
            max_right = maxp.query(1, 0, N, x2, y1)
            ans = max(ans, max_right - min_left)
        if y1 < y2:
            max_suf_left = seg.query(1, 1, N, x1, y1).suffix if x1 <= y1 else NINF
            max_pre_right = seg.query(1, 1, N, y1 + 1, y2).prefix if y1 + 1 <= y2 else NINF
            ans = max(ans, max_suf_left + max_pre_right)
    print(ans)