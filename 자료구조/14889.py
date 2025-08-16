import sys
sys.setrecursionlimit(10 ** 5)
input = sys.stdin.readline

class SegmentTreeBeats:
    def __init__(self, n, a):
        self.n = n
        self.tree = [None] * (4 * n)
        self.INF = 10 ** 18
        self.neg_inf = -self.INF
        self.build(1, 1, n, a)

    class Node:
        def __init__(self):
            self.min_val = 0
            self.max_val = 0
            self.sum_val = 0
            self.lazy_add = 0
            self.lazy_assign = None

    def build(self, node, l, r, a):
        self.tree[node] = self.Node()
        if l == r:
            self.tree[node].min_val = a[l]
            self.tree[node].max_val = a[l]
            self.tree[node].sum_val = a[l]
            return
        mid = (l + r) // 2
        self.build(2 * node, l, mid, a)
        self.build(2 * node + 1, mid + 1, r, a)
        self.pushup(node)

    def pushup(self, node):
        le = self.tree[2 * node]
        ri = self.tree[2 * node + 1]
        self.tree[node].min_val = min(le.min_val, ri.min_val)
        self.tree[node].max_val = max(le.max_val, ri.max_val)
        self.tree[node].sum_val = le.sum_val + ri.sum_val

    def propagate(self, node, l, r):
        if self.tree[node].lazy_assign is not None:
            assign_val = self.tree[node].lazy_assign
            self.tree[node].min_val = assign_val
            self.tree[node].max_val = assign_val
            self.tree[node].sum_val = assign_val * (r - l + 1)
            if l != r:
                self.tree[2 * node].lazy_assign = assign_val
                self.tree[2 * node].lazy_add = 0
                self.tree[2 * node + 1].lazy_assign = assign_val
                self.tree[2 * node + 1].lazy_add = 0
                self.tree[2 * node].min_val = assign_val
                self.tree[2 * node].max_val = assign_val
                self.tree[2 * node].sum_val = assign_val * ((l + r) // 2 - l + 1)
                self.tree[2 * node + 1].min_val = assign_val
                self.tree[2 * node + 1].max_val = assign_val
                self.tree[2 * node + 1].sum_val = assign_val * (r - (l + r) // 2)
            self.tree[node].lazy_assign = None
        if self.tree[node].lazy_add != 0:
            add_val = self.tree[node].lazy_add
            self.tree[node].min_val += add_val
            self.tree[node].max_val += add_val
            self.tree[node].sum_val += add_val * (r - l + 1)
            if l != r:
                self.tree[2 * node].lazy_add += add_val
                self.tree[2 * node + 1].lazy_add += add_val
            self.tree[node].lazy_add = 0

    def _update_div(self, node, l, r, start, end, d):
        self.propagate(node, l, r)
        if start > r or end < l:
            return
        minv = self.tree[node].min_val
        maxv = self.tree[node].max_val
        if start <= l and r <= end:
            if minv // d == maxv // d:
                floor_v = minv // d
                self.tree[node].lazy_assign = floor_v
                self.tree[node].lazy_add = 0
                self.propagate(node, l, r)
                return
            if minv + 1 == maxv:
                add_val = (minv // d) - minv
                self.tree[node].lazy_add += add_val
                self.propagate(node, l, r)
                return
        mid = (l + r) // 2
        self._update_div(2 * node, l, mid, start, end, d)
        self._update_div(2 * node + 1, mid + 1, r, start, end, d)
        self.pushup(node)

    def update_div(self, start, end, d):
        if d == 1:
            return
        self._update_div(1, 1, self.n, start, end, d)

    def _update_add(self, node, l, r, start, end, val):
        self.propagate(node, l, r)
        if start > r or end < l:
            return
        if start <= l and r <= end:
            self.tree[node].lazy_add += val
            self.propagate(node, l, r)
            return
        mid = (l + r) // 2
        self._update_add(2 * node, l, mid, start, end, val)
        self._update_add(2 * node + 1, mid + 1, r, start, end, val)
        self.pushup(node)

    def update_add(self, start, end, val):
        self._update_add(1, 1, self.n, start, end, val)

    def _query_min(self, node, l, r, start, end):
        self.propagate(node, l, r)
        if start > r or end < l:
            return self.INF
        if start <= l and r <= end:
            return self.tree[node].min_val
        mid = (l + r) // 2
        left_min = self._query_min(2 * node, l, mid, start, end)
        right_min = self._query_min(2 * node + 1, mid + 1, r, start, end)
        return min(left_min, right_min)

    def query_min(self, start, end):
        return self._query_min(1, 1, self.n, start, end)

    def _query_sum(self, node, l, r, start, end):
        self.propagate(node, l, r)
        if start > r or end < l:
            return 0
        if start <= l and r <= end:
            return self.tree[node].sum_val
        mid = (l + r) // 2
        left_sum = self._query_sum(2 * node, l, mid, start, end)
        right_sum = self._query_sum(2 * node + 1, mid + 1, r, start, end)
        return left_sum + right_sum

    def query_sum(self, start, end):
        return self._query_sum(1, 1, self.n, start, end)

def main():
    n, q = map(int, input().split())
    a = [0] + list(map(int, input().split()))
    st = SegmentTreeBeats(n, a)
    for _ in range(q):
        query = list(map(int, input().split()))
        op = query[0]
        if op == 1:
            l, r, c = query[1], query[2], query[3]
            st.update_add(l + 1, r + 1, c)
        elif op == 2:
            l, r, d = query[1], query[2], query[3]
            st.update_div(l + 1, r + 1, d)
        elif op == 3:
            l, r = query[1], query[2]
            print(st.query_min(l + 1, r + 1))
        elif op == 4:
            l, r = query[1], query[2]
            print(st.query_sum(l + 1, r + 1))

if __name__ == "__main__":
    main()