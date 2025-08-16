import sys
input = sys.stdin.readline

BIT = 31
MASK_BITS = (1 << 32) - 1

class TrieNode:
    def __init__(self):
        self.children = [None] * 2
        self.cnt = 0

class SegmentTree:
    def __init__(self, n, a, k):
        self.n = n
        self.K = k
        self.tree = [None] * (4 * n)
        self.lazy = [0] * (4 * n)
        self.build(1, 1, n, a)

    def build(self, node, l, r, a):
        self.tree[node] = TrieNode()
        if l == r:
            self.insert(self.tree[node], a[l])
            return
        mid = (l + r) // 2
        self.build(2 * node, l, mid, a)
        self.build(2 * node + 1, mid + 1, r, a)
        self.merge(self.tree[node], self.tree[2 * node], self.tree[2 * node + 1])

    def insert(self, root, val):
        cur = root
        cur.cnt += 1
        for b in range(BIT, -1, -1):
            idx = 1 if (val & (1 << b)) else 0
            if cur.children[idx] is None:
                cur.children[idx] = TrieNode()
            cur = cur.children[idx]
            cur.cnt += 1

    def merge(self, new, n1, n2):
        new.cnt = n1.cnt + n2.cnt
        for i in range(2):
            c1 = n1.children[i]
            c2 = n2.children[i]
            if c1 or c2:
                new.children[i] = TrieNode()
                if c1 and c2:
                    self.merge(new.children[i], c1, c2)
                elif c1:
                    new.children[i] = c1
                else:
                    new.children[i] = c2

    def push(self, node, l, r):
        if self.lazy[node] != 0:
            if l != r:
                self.lazy[2 * node] |= self.lazy[node]
                self.lazy[2 * node + 1] |= self.lazy[node]
            self.lazy[node] = 0

    def update(self, node, l, r, start, end, x):
        if start > r or end < l:
            return
        if start <= l and r <= end:
            self.lazy[node] |= x
            return
        self.push(node, l, r)
        mid = (l + r) // 2
        self.update(2 * node, l, mid, start, end, x)
        self.update(2 * node + 1, mid + 1, r, start, end, x)

    def query(self, node, l, r, start, end):
        if start > r or end < l:
            return 0
        if start <= l and r <= end:
            mask = self.lazy[node]
            if mask & (MASK_BITS ^ self.K):
                return 0
            m = MASK_BITS ^ mask
            v = self.K & m
            return self.get_count(self.tree[node], m, v, BIT)
        self.push(node, l, r)
        mid = (l + r) // 2
        return self.query(2 * node, l, mid, start, end) + self.query(2 * node + 1, mid + 1, r, start, end)

    def get_count(self, root, m, v, bit):
        if root is None:
            return 0
        if bit < 0:
            return root.cnt
        has_m = (m & (1 << bit)) != 0
        req = (v & (1 << bit)) != 0
        if has_m:
            child_idx = 1 if req else 0
            return self.get_count(root.children[child_idx], m, v, bit - 1)
        else:
            return self.get_count(root.children[0], m, v, bit - 1) + self.get_count(root.children[1], m, v, bit - 1)

N, K = map(int, input().split())
A = [0] + list(map(int, input().split()))
st = SegmentTree(N, A, K)
Q = int(input())
for _ in range(Q):
    line = list(map(int, input().split()))
    tp = line[0]
    l = line[1]
    r = line[2]
    if tp == 1:
        x = line[3]
        st.update(1, 1, N, l, r, x)
    else:
        print(st.query(1, 1, N, l, r))