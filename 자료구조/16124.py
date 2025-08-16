import sys
input = sys.stdin.readline

MOD = 998244353

class Node:
    def __init__(self, and_=0, or_=0, val=0):
        self.and_ = and_
        self.or_ = or_
        self.val = val

def f(a, b, sz):
    pw_half = pow(10, sz // 2, MOD)
    val = ((a.val * pw_half) % MOD + b.val) % MOD
    return Node(a.and_ & b.and_, a.or_ | b.or_, val)

def qf(a, b):
    if a[0] == -1:
        return b
    if b[0] == -1:
        return a
    pw_b = pow(10, b[1], MOD)
    val = ((a[0] * pw_b) % MOD + b[0]) % MOD
    return (val, a[1] + b[1])

class SegmentTree:
    def __init__(self, n, s):
        self.n = n
        self.tree = [Node() for _ in range(4 * n + 5)]
        self.lazy = [(-1, 0) for _ in range(4 * n + 5)]
        self.pw = [1] * (n + 1)
        self.sm = [0] * (n + 1)
        for i in range(1, n + 1):
            self.pw[i] = (self.pw[i - 1] * 10) % MOD
            self.sm[i] = (self.sm[i - 1] * 10 + 1) % MOD
        self.a = [0] * (n + 1)
        for i in range(1, n + 1):
            self.a[i] = int(s[i - 1])
        self.build(1, 1, n)

    def build(self, node, s, e):
        if s == e:
            d = self.a[s]
            self.tree[node] = Node(1 << d, 1 << d, d)
            return self.tree[node]
        m = (s + e) // 2
        left = self.build(2 * node, s, m)
        right = self.build(2 * node + 1, m + 1, e)
        self.tree[node] = f(left, right, e - s + 1)
        return self.tree[node]

    def push_lazy(self, node, s, e):
        fr, to = self.lazy[node]
        if fr == -1:
            return
        t = (self.sm[e - s + 1] * to) % MOD
        self.tree[node] = Node(1 << to, 1 << to, t)
        if s != e:
            self.lazy[2 * node] = (fr, to)
            self.lazy[2 * node + 1] = (fr, to)
        self.lazy[node] = (-1, 0)

    def update(self, node, s, e, l, r, fr, to):
        self.push_lazy(node, s, e)
        if r < s or e < l or not (self.tree[node].or_ & (1 << fr)):
            return
        if l <= s and e <= r and self.tree[node].and_ == (1 << fr):
            self.lazy[node] = (fr, to)
            self.push_lazy(node, s, e)
            return
        if s == e:
            return
        m = (s + e) // 2
        self.update(2 * node, s, m, l, r, fr, to)
        self.update(2 * node + 1, m + 1, e, l, r, fr, to)
        self.tree[node] = f(self.tree[2 * node], self.tree[2 * node + 1], e - s + 1)

    def query(self, node, s, e, l, r):
        self.push_lazy(node, s, e)
        if r < s or e < l:
            return (-1, 0)
        if l <= s and e <= r:
            return (self.tree[node].val % MOD, e - s + 1)
        m = (s + e) // 2
        left = self.query(2 * node, s, m, l, r)
        right = self.query(2 * node + 1, m + 1, e, l, r)
        return qf(left, right)

S = input().strip()
N = len(S)
st = SegmentTree(N, S)
Q = int(input())
for _ in range(Q):
    k,*args = list(map(int, input().split()))
    if k == 1:
        i, j, fr, to = args
        st.update(1, 1, N, i, j, fr, to)
    else:
        i, j = args
        print(st.query(1, 1, N, i, j)[0])