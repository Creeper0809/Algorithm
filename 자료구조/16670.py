import sys
import bisect

input = sys.stdin.readline

class SegmentTree:
    def __init__(self, n, T):
        self.n = n
        self.T = T
        self.tree_sum = [0] * (4 * (n + 1))
        self.tree_max = [0] * (4 * (n + 1))
        self.build(1, 1, n)

    def build(self, node, l, r):
        if l == r:
            self.tree_sum[node] = 0
            self.tree_max[node] = self.T[l - 1]
            return
        mid = (l + r) // 2
        self.build(2 * node, l, mid)
        self.build(2 * node + 1, mid + 1, r)
        self.tree_sum[node] = self.tree_sum[2 * node] + self.tree_sum[2 * node + 1]
        self.tree_max[node] = max(self.tree_max[2 * node + 1], self.tree_max[2 * node] + self.tree_sum[2 * node + 1])

    def update(self, idx, val):
        self._update(1, 1, self.n, idx, val)

    def _update(self, node, l, r, idx, val):
        if l == r:
            self.tree_sum[node] += val
            self.tree_max[node] += val
            return
        mid = (l + r) // 2
        if idx <= mid:
            self._update(2 * node, l, mid, idx, val)
        else:
            self._update(2 * node + 1, mid + 1, r, idx, val)
        self.tree_sum[node] = self.tree_sum[2 * node] + self.tree_sum[2 * node + 1]
        self.tree_max[node] = max(self.tree_max[2 * node + 1], self.tree_max[2 * node] + self.tree_sum[2 * node + 1])

    def query(self, x):
        if x < 1:
            return 0
        return self._query(1, 1, self.n, x, 0)

    def _query(self, node, l, r, x, ans):
        if r <= x:
            ans = max(self.tree_max[node], ans + self.tree_sum[node])
            return ans
        mid = (l + r) // 2
        ans = self._query(2 * node, l, mid, x, ans)
        if mid < x:
            ans = self._query(2 * node + 1, mid + 1, r, x, ans)
        return ans

q = int(input())
events = []
t_set = set()
for _ in range(q):
    line = input().strip().split()
    events.append(line)
    if line[0] in ['+', '?']:
        t_set.add(int(line[1]))

T = sorted(list(t_set))
m = len(T)
rank = {T[i]: i + 1 for i in range(m)}

st = SegmentTree(m, T)
event_info = [None] * (q + 1)

for event_num in range(1, q + 1):
    line = events[event_num - 1]
    typ = line[0]
    if typ == '+':
        t = int(line[1])
        d = int(line[2])
        event_info[event_num] = (t, d)
        r = rank[t]
        st.update(r, d)
    elif typ == '-':
        i = int(line[1])
        t, d = event_info[i]
        r = rank[t]
        st.update(r, -d)
    elif typ == '?':
        qp = int(line[1])
        idx = bisect.bisect_right(T, qp)
        ans = st.query(idx)
        print(max(ans - qp, 0))