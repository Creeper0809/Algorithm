import sys

class Node:
    def __init__(self):
        self.max_len = 0
        self.prefix_len = 0
        self.suffix_len = 0
        self.prefix_val = 0
        self.suffix_val = 0
        self.total_len = 0

class SegmentTree:
    def __init__(self, n, d):
        self.n = n
        self.tree = [Node() for _ in range(4 * n + 4)]
        self.lazy = [0] * (4 * n + 4)
        self.build(1, 1, n, d)

    def build(self, node, l, r, d):
        if l == r:
            self.tree[node].max_len = 1
            self.tree[node].prefix_len = 1
            self.tree[node].suffix_len = 1
            self.tree[node].prefix_val = d[l]
            self.tree[node].suffix_val = d[l]
            self.tree[node].total_len = 1
            return
        mid = (l + r) // 2
        self.build(2 * node, l, mid, d)
        self.build(2 * node + 1, mid + 1, r, d)
        self.merge(node)

    def merge(self, node):
        left = self.tree[2 * node]
        right = self.tree[2 * node + 1]
        res = self.tree[node]
        res.total_len = left.total_len + right.total_len
        res.max_len = max(left.max_len, right.max_len)
        if left.suffix_val == right.prefix_val:
            res.max_len = max(res.max_len, left.suffix_len + right.prefix_len)
        res.prefix_len = left.prefix_len
        res.prefix_val = left.prefix_val
        if left.prefix_len == left.total_len and left.suffix_val == right.prefix_val:
            res.prefix_len += right.prefix_len
        res.suffix_len = right.suffix_len
        res.suffix_val = right.suffix_val
        if right.suffix_len == right.total_len and right.prefix_val == left.suffix_val:
            res.suffix_len += left.suffix_len

    def push(self, node, l, r):
        if self.lazy[node] != 0:
            self.tree[node].prefix_val += self.lazy[node]
            self.tree[node].suffix_val += self.lazy[node]
            if l != r:
                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]
            self.lazy[node] = 0

    def update(self, start, end, val):
        self._update(1, 1, self.n, start, end, val)

    def _update(self, node, l, r, start, end, val):
        self.push(node, l, r)
        if start > r or end < l:
            return
        if start <= l and r <= end:
            self.lazy[node] += val
            self.push(node, l, r)
            return
        mid = (l + r) // 2
        self._update(2 * node, l, mid, start, end, val)
        self._update(2 * node + 1, mid + 1, r, start, end, val)
        self.merge(node)

    def query(self, start, end):
        res = self._query(1, 1, self.n, start, end)
        return res

    def _query(self, node, l, r, start, end):
        self.push(node, l, r)
        if start > r or end < l:
            return None
        if start <= l and r <= end:
            return self.tree[node]
        mid = (l + r) // 2
        left_q = self._query(2 * node, l, mid, start, end)
        right_q = self._query(2 * node + 1, mid + 1, r, start, end)
        if left_q is None:
            return right_q
        if right_q is None:
            return left_q
        res = Node()
        res.total_len = left_q.total_len + right_q.total_len
        res.max_len = max(left_q.max_len, right_q.max_len)
        if left_q.suffix_val == right_q.prefix_val:
            res.max_len = max(res.max_len, left_q.suffix_len + right_q.prefix_len)
        res.prefix_len = left_q.prefix_len
        res.prefix_val = left_q.prefix_val
        if left_q.prefix_len == left_q.total_len and left_q.suffix_val == right_q.prefix_val:
            res.prefix_len += right_q.prefix_len
        res.suffix_len = right_q.suffix_len
        res.suffix_val = right_q.suffix_val
        if right_q.suffix_len == right_q.total_len and right_q.prefix_val == left_q.suffix_val:
            res.suffix_len += left_q.suffix_len
        return res

input = sys.stdin.readline
N = int(input())
A = list(map(int, input().split()))
A = [0] + A
D = [0] * N
for k in range(1, N):
    D[k] = A[k + 1] - A[k]
st = SegmentTree(N - 1, D)
M = int(input())
for _ in range(M):
    q = list(map(int, input().split()))
    if q[0] == 1:
        i, j, x, y = q[1], q[2], q[3], q[4]
        if i > 1:
            st.update(i - 1, i - 1, x)
        if j < N:
            delta = x + y * (j - i)
            st.update(j, j, -delta)
        if i < j:
            st.update(i, j - 1, y)
    else:
        i, j = q[1], q[2]
        res = st.query(i, j - 1)
        print(res.max_len + 1)