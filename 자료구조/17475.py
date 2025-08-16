import sys
input = sys.stdin.readline

inf = 10**18

class HistVal:
    def __init__(self):
        self.min_v = inf
        self.smin_v = inf
        self.min_c = 0
        self.min_s = 0
        self.m_hmax = -inf
        self.nm_hmax = -inf
        self.max_v = -inf
        self.smax_v = -inf
        self.max_c = 0
        self.max_s = 0
        self.m_hmin = inf
        self.nm_hmin = inf

    def init(self, x):
        self.min_v = 0
        self.smin_v = inf
        self.min_c = 1
        self.m_hmax = x
        self.nm_hmax = -inf
        self.max_v = 0
        self.smax_v = -inf
        self.max_c = 1
        self.m_hmin = x
        self.nm_hmin = inf
        self.min_s = 0
        self.max_s = 0

    def init_empty(self):
        self.min_v = inf
        self.smin_v = inf
        self.min_c = 0
        self.m_hmax = -inf
        self.nm_hmax = -inf
        self.max_v = -inf
        self.smax_v = -inf
        self.max_c = 0
        self.m_hmin = inf
        self.nm_hmin = inf
        self.min_s = 0
        self.max_s = 0

    def update_min(self, x):
        if self.min_v < x:
            self.min_s += (x - self.min_v) * self.min_c
            self.m_hmax += (x - self.min_v)
            self.min_v = x

    def update_max(self, x):
        if x < self.max_v:
            self.max_s += (x - self.max_v) * self.max_c
            self.m_hmin += (x - self.max_v)
            self.max_v = x

    def update(self, v):
        self.update_min(v.min_v)
        self.update_max(v.max_v)

    def merge(self, l, r):
        self.min_s = l.min_s + r.min_s
        self.nm_hmax = max(l.nm_hmax, r.nm_hmax)
        if l.min_v < r.min_v:
            self.smin_v = min(l.smin_v, r.min_v)
            self.min_v = l.min_v
            self.min_c = l.min_c
            self.nm_hmax = max(self.nm_hmax, r.m_hmax)
            self.m_hmax = l.m_hmax
        elif l.min_v > r.min_v:
            self.smin_v = min(l.min_v, r.smin_v)
            self.min_v = r.min_v
            self.min_c = r.min_c
            self.nm_hmax = max(self.nm_hmax, l.m_hmax)
            self.m_hmax = r.m_hmax
        else:
            self.smin_v = min(l.smin_v, r.smin_v)
            self.min_v = l.min_v
            self.min_c = l.min_c + r.min_c
            self.m_hmax = max(l.m_hmax, r.m_hmax)
        self.max_s = l.max_s + r.max_s
        self.nm_hmin = min(l.nm_hmin, r.nm_hmin)
        if l.max_v > r.max_v:
            self.smax_v = max(l.smax_v, r.max_v)
            self.max_v = l.max_v
            self.max_c = l.max_c
            self.nm_hmin = min(self.nm_hmin, r.m_hmin)
            self.m_hmin = l.m_hmin
        elif l.max_v < r.max_v:
            self.smax_v = max(l.max_v, r.smax_v)
            self.max_v = r.max_v
            self.max_c = r.max_c
            self.nm_hmin = min(self.nm_hmin, l.m_hmin)
            self.m_hmin = r.m_hmin
        else:
            self.smax_v = max(l.smax_v, r.smax_v)
            self.max_v = l.max_v
            self.max_c = l.max_c + r.max_c
            self.m_hmin = min(l.m_hmin, r.m_hmin)

    def add(self, x, c):
        if self.min_v != inf:
            self.min_v += x
        if self.smin_v != inf:
            self.smin_v += x
        self.min_s += x * c
        if self.max_v != -inf:
            self.max_v += x
        if self.smax_v != -inf:
            self.smax_v += x
        self.max_s += x * c

    def hmax(self):
        return max(self.m_hmax, self.nm_hmax)

    def hmin(self):
        return min(self.m_hmin, self.nm_hmin)

N = 500010
class SegmentTree:
    def __init__(self, n, a):
        self.inf = inf
        self.n0 = 1
        while self.n0 < n:
            self.n0 <<= 1
        self.len = [0] * (4 * N)
        self.ladd = [0] * (4 * N)
        self.max_d = [HistVal() for _ in range(4 * N)]
        self.nval_d = [HistVal() for _ in range(4 * N)]
        self.min_d = [HistVal() for _ in range(4 * N)]
        self.max_v = [0] * (4 * N)
        self.smax_v = [0] * (4 * N)
        self.max_c = [0] * (4 * N)
        self.min_v = [0] * (4 * N)
        self.smin_v = [0] * (4 * N)
        self.min_c = [0] * (4 * N)
        self.sum = [0] * (4 * N)

        self.len[0] = self.n0
        for i in range(self.n0 - 1):
            self.len[2 * i + 1] = self.len[2 * i + 2] = (self.len[i] >> 1)
        for i in range(n):
            self.max_v[self.n0 - 1 + i] = self.min_v[self.n0 - 1 + i] = self.sum[self.n0 - 1 + i] = a[i]
            self.smax_v[self.n0 - 1 + i] = -self.inf
            self.smin_v[self.n0 - 1 + i] = self.inf
            self.max_c[self.n0 - 1 + i] = self.min_c[self.n0 - 1 + i] = 1
            self.max_d[self.n0 - 1 + i].init(a[i])
            self.nval_d[self.n0 - 1 + i].init_empty()
            self.min_d[self.n0 - 1 + i].init(a[i])
        for i in range(n, self.n0):
            self.sum[self.n0 - 1 + i] = 0
            self.max_v[self.n0 - 1 + i] = self.smax_v[self.n0 - 1 + i] = -self.inf
            self.min_v[self.n0 - 1 + i] = self.smin_v[self.n0 - 1 + i] = self.inf
            self.max_c[self.n0 - 1 + i] = self.min_c[self.n0 - 1 + i] = 0
            self.max_d[self.n0 - 1 + i].init_empty()
            self.nval_d[self.n0 - 1 + i].init_empty()
            self.min_d[self.n0 - 1 + i].init_empty()
        for i in range(self.n0 - 2, -1, -1):
            self._update(i)

    def _update_node_max(self, k, x):
        self.sum[k] += (x - self.max_v[k]) * self.max_c[k]
        self.max_d[k].add(self.max_v[k] - x, self.max_c[k])
        if self.max_v[k] == self.min_v[k]:
            self.min_d[k].add(self.min_v[k] - x, self.min_c[k])
            self.max_v[k] = self.min_v[k] = x
        elif self.max_v[k] == self.smin_v[k]:
            self.max_v[k] = self.smin_v[k] = x
        else:
            self.max_v[k] = x

    def _update_node_min(self, k, x):
        self.sum[k] += (x - self.min_v[k]) * self.min_c[k]
        self.min_d[k].add(self.min_v[k] - x, self.min_c[k])
        if self.min_v[k] == self.max_v[k]:
            self.max_d[k].add(self.max_v[k] - x, self.max_c[k])
            self.min_v[k] = self.max_v[k] = x
        elif self.min_v[k] == self.smax_v[k]:
            self.min_v[k] = self.smax_v[k] = x
        else:
            self.min_v[k] = x

    def _addall(self, k, a):
        self.sum[k] += a * self.len[k]
        self.max_v[k] += a
        if self.smax_v[k] != -self.inf:
            self.smax_v[k] += a
        self.min_v[k] += a
        if self.smin_v[k] != self.inf:
            self.smin_v[k] += a
        self.max_d[k].add(-a, self.max_c[k])
        if self.max_v[k] != self.min_v[k]:
            self.nval_d[k].add(-a, self.len[k] - self.min_c[k] - self.max_c[k])
        self.min_d[k].add(-a, self.min_c[k])
        self.ladd[k] += a

    def _push_hist(self, p, k):
        if self.min_v[k] == self.min_v[p]:
            self.min_d[p].update(self.min_d[k])
        elif self.max_v[k] == self.min_v[p]:
            self.min_d[p].update(self.max_d[k])
        else:
            self.min_d[p].update(self.nval_d[k])
        if self.max_v[k] == self.max_v[p]:
            self.max_d[p].update(self.max_d[k])
        elif self.min_v[k] == self.max_v[p]:
            self.max_d[p].update(self.min_d[k])
        else:
            self.max_d[p].update(self.nval_d[k])
        self.nval_d[p].update(self.nval_d[k])

    def _push(self, k):
        if k >= self.n0 - 1:
            return
        if self.ladd[k] != 0:
            self._addall(2 * k + 1, self.ladd[k])
            self._addall(2 * k + 2, self.ladd[k])
            self.ladd[k] = 0
        if self.max_v[k] < self.max_v[2 * k + 1]:
            self._update_node_max(2 * k + 1, self.max_v[k])
        if self.max_v[k] < self.max_v[2 * k + 2]:
            self._update_node_max(2 * k + 2, self.max_v[k])
        if self.min_v[2 * k + 1] < self.min_v[k]:
            self._update_node_min(2 * k + 1, self.min_v[k])
        if self.min_v[2 * k + 2] < self.min_v[k]:
            self._update_node_min(2 * k + 2, self.min_v[k])
        self._push_hist(2 * k + 1, k)
        self._push_hist(2 * k + 2, k)

    def _update(self, k):
        self.sum[k] = self.sum[2 * k + 1] + self.sum[2 * k + 2]
        self.nval_d[k].merge(self.nval_d[2 * k + 1], self.nval_d[2 * k + 2])
        if self.max_v[2 * k + 1] > self.max_v[2 * k + 2]:
            self.max_v[k] = self.max_v[2 * k + 1]
            self.max_c[k] = self.max_c[2 * k + 1]
            self.smax_v[k] = max(self.smax_v[2 * k + 1], self.max_v[2 * k + 2])
            self.max_d[k] = self.max_d[2 * k + 1]  # 객체 복사 주의, 하지만 파이썬에서는 참조
        elif self.max_v[2 * k + 1] < self.max_v[2 * k + 2]:
            self.max_v[k] = self.max_v[2 * k + 2]
            self.max_c[k] = self.max_c[2 * k + 2]
            self.smax_v[k] = max(self.max_v[2 * k + 1], self.smax_v[2 * k + 2])
            self.max_d[k] = self.max_d[2 * k + 2]
        else:
            self.max_v[k] = self.max_v[2 * k + 1]
            self.max_c[k] = self.max_c[2 * k + 1] + self.max_c[2 * k + 2]
            self.smax_v[k] = max(self.smax_v[2 * k + 1], self.smax_v[2 * k + 2])
            self.max_d[k].merge(self.max_d[2 * k + 1], self.max_d[2 * k + 2])
        if self.min_v[2 * k + 1] < self.min_v[2 * k + 2]:
            self.min_v[k] = self.min_v[2 * k + 1]
            self.min_c[k] = self.min_c[2 * k + 1]
            self.smin_v[k] = min(self.smin_v[2 * k + 1], self.min_v[2 * k + 2])
            self.min_d[k] = self.min_d[2 * k + 1]
        elif self.min_v[2 * k + 1] > self.min_v[2 * k + 2]:
            self.min_v[k] = self.min_v[2 * k + 2]
            self.min_c[k] = self.min_c[2 * k + 2]
            self.smin_v[k] = min(self.min_v[2 * k + 1], self.smin_v[2 * k + 2])
            self.min_d[k] = self.min_d[2 * k + 2]
        else:
            self.min_v[k] = self.min_v[2 * k + 1]
            self.min_c[k] = self.min_c[2 * k + 1] + self.min_c[2 * k + 2]
            self.smin_v[k] = min(self.smin_v[2 * k + 1], self.smin_v[2 * k + 2])
            self.min_d[k].merge(self.min_d[2 * k + 1], self.min_d[2 * k + 2])
        if self.min_v[2 * k + 1] == self.max_v[2 * k + 1]:
            if self.min_v[k] < self.min_v[2 * k + 1] and self.max_v[2 * k + 1] < self.max_v[k]:
                self.nval_d[k].merge(self.nval_d[k], self.max_d[2 * k + 1])
        else:
            if self.max_v[2 * k + 1] < self.max_v[k]:
                self.nval_d[k].merge(self.nval_d[k], self.max_d[2 * k + 1])
            if self.min_v[k] < self.min_v[2 * k + 1]:
                self.nval_d[k].merge(self.nval_d[k], self.min_d[2 * k + 1])
        if self.min_v[2 * k + 2] == self.max_v[2 * k + 2]:
            if self.min_v[k] < self.min_v[2 * k + 2] and self.max_v[2 * k + 2] < self.max_v[k]:
                self.nval_d[k].merge(self.nval_d[k], self.max_d[2 * k + 2])
        else:
            if self.max_v[2 * k + 2] < self.max_v[k]:
                self.nval_d[k].merge(self.nval_d[k], self.max_d[2 * k + 2])
            if self.min_v[k] < self.min_v[2 * k + 2]:
                self.nval_d[k].merge(self.nval_d[k], self.min_d[2 * k + 2])

    def _update_min(self, x, a, b, k, l, r):
        if b <= l or r <= a or self.max_v[k] <= x:
            return
        if a <= l and r <= b and self.smax_v[k] < x:
            self._update_node_max(k, x)
            self._update_dmax(k, l, r)
            self._update_dmin(k, l, r)
            return
        self._push(k)
        self._update_min(x, a, b, 2 * k + 1, l, (l + r) // 2)
        self._update_min(x, a, b, 2 * k + 2, (l + r) // 2, r)
        self._update(k)

    def _update_max(self, x, a, b, k, l, r):
        if b <= l or r <= a or x <= self.min_v[k]:
            return
        if a <= l and r <= b and x < self.smin_v[k]:
            self._update_node_min(k, x)
            self._update_dmax(k, l, r)
            self._update_dmin(k, l, r)
            return
        self._push(k)
        self._update_max(x, a, b, 2 * k + 1, l, (l + r) // 2)
        self._update_max(x, a, b, 2 * k + 2, (l + r) // 2, r)
        self._update(k)

    def _update_dmax(self, k, l, r):
        if l == r or (0 <= self.max_d[k].min_v and 0 <= self.nval_d[k].min_v and 0 <= self.min_d[k].min_v):
            return
        if 0 < self.max_d[k].smin_v and 0 < self.nval_d[k].smin_v and 0 < self.min_d[k].smin_v:
            self.max_d[k].update_min(0)
            self.nval_d[k].update_min(0)
            self.min_d[k].update_min(0)
            return
        self._push(k)
        self._update_dmax(2 * k + 1, l, (l + r) // 2)
        self._update_dmax(2 * k + 2, (l + r) // 2, r)
        self._update(k)

    def _update_dmin(self, k, l, r):
        if l == r or (self.max_d[k].max_v <= 0 and self.nval_d[k].max_v <= 0 and self.min_d[k].max_v <= 0):
            return
        if self.max_d[k].smax_v < 0 and self.nval_d[k].smax_v < 0 and self.min_d[k].smax_v < 0:
            self.max_d[k].update_max(0)
            self.nval_d[k].update_max(0)
            self.min_d[k].update_max(0)
            return
        self._push(k)
        self._update_dmin(2 * k + 1, l, (l + r) // 2)
        self._update_dmin(2 * k + 2, (l + r) // 2, r)
        self._update(k)

    def _add_val(self, x, a, b, k, l, r):
        if b <= l or r <= a:
            return
        if a <= l and r <= b:
            self._addall(k, x)
            self._update_dmax(k, l, r)
            self._update_dmin(k, l, r)
            return
        self._push(k)
        self._add_val(x, a, b, 2 * k + 1, l, (l + r) // 2)
        self._add_val(x, a, b, 2 * k + 2, (l + r) // 2, r)
        self._update(k)

    def _query_max(self, a, b, k, l, r):
        if b <= l or r <= a:
            return -self.inf
        if a <= l and r <= b:
            return self.max_v[k]
        self._push(k)
        lv = self._query_max(a, b, 2 * k + 1, l, (l + r) // 2)
        rv = self._query_max(a, b, 2 * k + 2, (l + r) // 2, r)
        return max(lv, rv)

    def _query_min(self, a, b, k, l, r):
        if b <= l or r <= a:
            return self.inf
        if a <= l and r <= b:
            return self.min_v[k]
        self._push(k)
        lv = self._query_min(a, b, 2 * k + 1, l, (l + r) // 2)
        rv = self._query_min(a, b, 2 * k + 2, (l + r) // 2, r)
        return min(lv, rv)

    def _query_hmax_max(self, a, b, k, l, r):
        if b <= l or r <= a:
            return -self.inf
        if a <= l and r <= b:
            return max(self.max_d[k].hmax(), self.min_d[k].hmax(), self.nval_d[k].hmax())
        self._push(k)
        lv = self._query_hmax_max(a, b, 2 * k + 1, l, (l + r) // 2)
        rv = self._query_hmax_max(a, b, 2 * k + 2, (l + r) // 2, r)
        return max(lv, rv)

    def _query_hmin_min(self, a, b, k, l, r):
        if b <= l or r <= a:
            return self.inf
        if a <= l and r <= b:
            return min(self.max_d[k].hmin(), self.min_d[k].hmin(), self.nval_d[k].hmin())
        self._push(k)
        lv = self._query_hmin_min(a, b, 2 * k + 1, l, (l + r) // 2)
        rv = self._query_hmin_min(a, b, 2 * k + 2, (l + r) // 2, r)
        return min(lv, rv)

    def _query_hmax_sum(self, a, b, k, l, r):
        if b <= l or r <= a:
            return 0
        if a <= l and r <= b:
            if self.max_v[k] == self.min_v[k]:
                return self.sum[k] + self.max_d[k].min_s
            return self.sum[k] + self.max_d[k].min_s + self.nval_d[k].min_s + self.min_d[k].min_s
        self._push(k)
        lv = self._query_hmax_sum(a, b, 2 * k + 1, l, (l + r) // 2)
        rv = self._query_hmax_sum(a, b, 2 * k + 2, (l + r) // 2, r)
        return lv + rv

    def _query_hmin_sum(self, a, b, k, l, r):
        if b <= l or r <= a:
            return 0
        if a <= l and r <= b:
            if self.max_v[k] == self.min_v[k]:
                return self.sum[k] + self.max_d[k].max_s
            return self.sum[k] + self.max_d[k].max_s + self.nval_d[k].max_s + self.min_d[k].max_s
        self._push(k)
        lv = self._query_hmin_sum(a, b, 2 * k + 1, l, (l + r) // 2)
        rv = self._query_hmin_sum(a, b, 2 * k + 2, (l + r) // 2, r)
        return lv + rv

    def update_min(self, a, b, x):
        self._update_min(x, a, b, 0, 0, self.n0)

    def update_max(self, a, b, x):
        self._update_max(x, a, b, 0, 0, self.n0)

    def add_val(self, a, b, x):
        self._add_val(x, a, b, 0, 0, self.n0)

    def update_val(self, a, b, x):
        self.update_min(a, b, x)
        self.update_max(a, b, x)

    def query_hmax_max(self, a, b):
        return self._query_hmax_max(a, b, 0, 0, self.n0)

    def query_hmax_sum(self, a, b):
        return self._query_hmax_sum(a, b, 0, 0, self.n0)

    def query_hmin_min(self, a, b):
        return self._query_hmin_min(a, b, 0, 0, self.n0)

    def query_hmin_sum(self, a, b):
        return self._query_hmin_sum(a, b, 0, 0, self.n0)

    def query_max(self, a, b):
        return self._query_max(a, b, 0, 0, self.n0)

    def query_min(self, a, b):
        return self._query_min(a, b, 0, 0, self.n0)

if __name__ == '__main__':
    nn = int(input().strip())
    aa = list(map(int, input().strip().split()))
    stb = SegmentTree(nn, aa)
    mm = int(input().strip())
    for _ in range(mm):
        query = list(map(int, input().strip().split()))
        typ = query[0]
        if typ == 1:
            l = query[1] - 1
            rr = query[2]
            xx = query[3]
            stb.add_val(l, rr, xx)
        elif typ == 2:
            l = query[1] - 1
            rr = query[2]
            yy = query[3]
            stb.update_max(l, rr, yy)
        elif typ == 3:
            l = query[1] - 1
            rr = query[2]
            yy = query[3]
            stb.update_min(l, rr, yy)
        elif typ == 4:
            ll = query[1] - 1
            rr = query[2]
            print(stb.query_min(ll, rr))
        elif typ == 5:
            ll = query[1] - 1
            rr = query[2]
            print(stb.query_hmin_min(ll, rr))
        elif typ == 6:
            ll = query[1] - 1
            rr = query[2]
            print(stb.query_hmax_max(ll, rr))