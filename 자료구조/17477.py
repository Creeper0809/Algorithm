import sys
import random
import math

# 빠른 입력을 위한 설정
input = sys.stdin.readline


class SegmentTreeBeats:
    class Node:
        def __init__(self):
            self.sum = 0
            self.sum_b = 0
            self.max_v = 0
            self.smax_v = 0
            self.max_c = 0
            self.min_v = 0
            self.smin_v = 0
            self.min_c = 0
            self.min_a = 0
            self.max_a = 0
            self.add_v = 0  # 범위 덧셈을 위한 lazy 태그 추가

    def __init__(self, n, a=None):
        self.n = n
        self.inf = 10 ** 18
        self.tree = [self.Node() for _ in range(4 * n + 4)]
        if a is None:
            a = [0] * (n + 1)
        self.build(1, 1, n, a)

    def build(self, k, l, r, a):
        if l == r:
            self.tree[k].sum = a[l]
            self.tree[k].max_v = a[l]
            self.tree[k].smax_v = -self.inf
            self.tree[k].max_c = 1
            self.tree[k].min_v = a[l]
            self.tree[k].smin_v = self.inf
            self.tree[k].min_c = 1
            # sum_b, min_a, max_a, add_v 는 0으로 초기화
            return
        mid = (l + r) // 2
        self.build(2 * k, l, mid, a)
        self.build(2 * k + 1, mid + 1, r, a)
        self.update(k)

    def _apply_add(self, k, l, r, val):
        node = self.tree[k]
        node.sum += (r - l + 1) * val
        node.max_v += val
        if node.smax_v != -self.inf: node.smax_v += val
        node.min_v += val
        if node.smin_v != self.inf: node.smin_v += val
        node.add_v += val

    def update_node_max(self, k, x):
        node = self.tree[k]
        diff = x - node.max_v
        if node.max_v == node.min_v:
            node.sum += diff * node.max_c
            node.max_v = node.min_v = x
        elif node.max_v == node.smin_v:
            node.sum += diff * node.max_c
            node.max_v = node.smin_v = x
        else:
            node.sum += diff * node.max_c
            node.max_v = x

    def update_node_min(self, k, x):
        node = self.tree[k]
        diff = x - node.min_v
        if node.min_v == node.max_v:
            node.sum += diff * node.min_c
            node.min_v = node.max_v = x
        elif node.min_v == node.smax_v:
            node.sum += diff * node.min_c
            node.min_v = node.smax_v = x
        else:
            node.sum += diff * node.min_c
            node.min_v = x

    def add_b(self, p, k, mi, ma):
        node = self.tree[k]
        p_node = self.tree[p]
        if p == 0 or p_node.min_v == node.min_v:
            node.sum_b += mi * node.min_c
            node.min_a += mi
        if p == 0 or p_node.max_v == node.max_v:
            node.sum_b += ma * node.max_c
            node.max_a += ma

    def push(self, k, l, r):
        left, right = 2 * k, 2 * k + 1
        mid = (l + r) // 2
        node = self.tree[k]

        # 1. 범위 덧셈 lazy 태그 전파
        if node.add_v != 0:
            self._apply_add(left, l, mid, node.add_v)
            self._apply_add(right, mid + 1, r, node.add_v)
            node.add_v = 0

        # 2. 범위 최솟/최댓값 lazy 태그 전파
        if node.max_v < self.tree[left].max_v:
            self.update_node_max(left, node.max_v)
        if self.tree[left].min_v < node.min_v:
            self.update_node_min(left, node.min_v)

        if node.max_v < self.tree[right].max_v:
            self.update_node_max(right, node.max_v)
        if self.tree[right].min_v < node.min_v:
            self.update_node_min(right, node.min_v)

        # 3. B 배열 변경 횟수 lazy 태그 전파
        if node.min_a != 0 or node.max_a != 0:
            self.add_b(k, left, node.min_a, node.max_a)
            self.add_b(k, right, node.min_a, node.max_a)
            node.min_a = node.max_a = 0

    def update(self, k):
        left, right = 2 * k, 2 * k + 1
        le, ri = self.tree[left], self.tree[right]
        node = self.tree[k]

        node.sum = le.sum + ri.sum
        node.sum_b = le.sum_b + ri.sum_b

        if le.max_v > ri.max_v:
            node.max_v = le.max_v
            node.max_c = le.max_c
            node.smax_v = max(le.smax_v, ri.max_v)
        elif le.max_v < ri.max_v:
            node.max_v = ri.max_v
            node.max_c = ri.max_c
            node.smax_v = max(ri.smax_v, le.max_v)
        else:
            node.max_v = le.max_v
            node.max_c = le.max_c + ri.max_c
            node.smax_v = max(le.smax_v, ri.smax_v)

        if le.min_v < ri.min_v:
            node.min_v = le.min_v
            node.min_c = le.min_c
            node.smin_v = min(le.smin_v, ri.min_v)
        elif le.min_v > ri.min_v:
            node.min_v = ri.min_v
            node.min_c = ri.min_c
            node.smin_v = min(ri.smin_v, le.min_v)
        else:
            node.min_v = le.min_v
            node.min_c = le.min_c + ri.min_c
            node.smin_v = min(le.smin_v, ri.smin_v)

    def _update_add(self, k, l, r, a, b, x):
        if b < l or r < a:
            return
        if a <= l and r <= b:
            self._apply_add(k, l, r, x)
            return

        self.push(k, l, r)
        mid = (l + r) // 2
        self._update_add(2 * k, l, mid, a, b, x)
        self._update_add(2 * k + 1, mid + 1, r, a, b, x)
        self.update(k)

    def update_add(self, a, b, x):
        self._update_add(1, 1, self.n, a, b, x)

    def _update_chmin(self, k, l, r, a, b, x):
        if b < l or r < a or self.tree[k].max_v <= x:
            return
        if a <= l and r <= b and self.tree[k].smax_v < x:
            # chmin으로 인해 최댓값이 변경되는 경우, B배열 변경 횟수 추가
            self.add_b(0, k, 0, 1)
            self.update_node_max(k, x)
            return

        self.push(k, l, r)
        mid = (l + r) // 2
        self._update_chmin(2 * k, l, mid, a, b, x)
        self._update_chmin(2 * k + 1, mid + 1, r, a, b, x)
        self.update(k)

    def update_chmin(self, a, b, x):
        self._update_chmin(1, 1, self.n, a, b, x)

    def _update_chmax(self, k, l, r, a, b, x):
        if b < l or r < a or x <= self.tree[k].min_v:
            return
        if a <= l and r <= b and x < self.tree[k].smin_v:
            # chmax로 인해 최솟값이 변경되는 경우, B배열 변경 횟수 추가
            self.add_b(0, k, 1, 0)
            self.update_node_min(k, x)
            return

        self.push(k, l, r)
        mid = (l + r) // 2
        self._update_chmax(2 * k, l, mid, a, b, x)
        self._update_chmax(2 * k + 1, mid + 1, r, a, b, x)
        self.update(k)

    def update_chmax(self, a, b, x):
        self._update_chmax(1, 1, self.n, a, b, x)

    def _query_sum_b(self, k, l, r, a, b):
        if b < l or r < a:
            return 0
        if a <= l and r <= b:
            return self.tree[k].sum_b

        self.push(k, l, r)
        mid = (l + r) // 2
        lv = self._query_sum_b(2 * k, l, mid, a, b)
        rv = self._query_sum_b(2 * k + 1, mid + 1, r, a, b)
        return lv + rv

    def query_sum_b(self, a, b):
        return self._query_sum_b(1, 1, self.n, a, b)


# 범위 덧셈 쿼리(타입 1)로 인한 B배열 값 증가를 관리하는 별도의 세그먼트 트리
class LazySegTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n + 4)
        self.lazy = [0] * (4 * n + 4)

    def _push(self, k, l, r):
        if self.lazy[k] == 0:
            return
        self.tree[k] += self.lazy[k] * (r - l + 1)
        if l != r:
            self.lazy[2 * k] += self.lazy[k]
            self.lazy[2 * k + 1] += self.lazy[k]
        self.lazy[k] = 0

    def _add(self, k, l, r, a, b, val):
        self._push(k, l, r)
        if b < l or r < a:
            return
        if a <= l and r <= b:
            self.lazy[k] += val
            self._push(k, l, r)
            return

        mid = (l + r) // 2
        self._add(2 * k, l, mid, a, b, val)
        self._add(2 * k + 1, mid + 1, r, a, b, val)
        self.tree[k] = self.tree[2 * k] + self.tree[2 * k + 1]

    def add(self, a, b, val):
        self._add(1, 1, self.n, a, b, val)

    def _query_sum(self, k, l, r, a, b):
        self._push(k, l, r)
        if b < l or r < a:
            return 0
        if a <= l and r <= b:
            return self.tree[k]

        mid = (l + r) // 2
        lv = self._query_sum(2 * k, l, mid, a, b)
        rv = self._query_sum(2 * k + 1, mid + 1, r, a, b)
        return lv + rv

    def query_sum(self, a, b):
        return self._query_sum(1, 1, self.n, a, b)


def main():
    N = int(input())
    initial_A = list(map(int, input().split()))
    # 1-based indexing으로 맞추기 위해 앞에 0 추가
    A = [0] + initial_A

    stb = SegmentTreeBeats(N, A)
    b_add_tree = LazySegTree(N)  # 타입 1 쿼리를 위한 B배열 관리 트리

    M = int(input())
    for _ in range(M):
        query = list(map(int, input().split()))
        q_type = query[0]

        if q_type == 1:  # 범위 덧셈
            L, R, X = query[1], query[2], query[3]
            stb.update_add(L, R, X)
            if X != 0:  # 0을 더하는 것은 값이 변하지 않음
                b_add_tree.add(L, R, 1)

        elif q_type == 2:  # 범위 최댓값으로 변경
            L, R, Y = query[1], query[2], query[3]
            stb.update_chmax(L, R, Y)

        elif q_type == 3:  # 범위 최솟값으로 변경
            L, R, Y = query[1], query[2], query[3]
            stb.update_chmin(L, R, Y)

        elif q_type == 4:  # B 배열의 구간 합 출력
            L, R = query[1], query[2]
            # chmin/chmax로 인한 변경 횟수 + range add로 인한 변경 횟수
            sum_b_ch = stb.query_sum_b(L, R)
            sum_b_add = b_add_tree.query_sum(L, R)
            print(sum_b_ch + sum_b_add)


if __name__ == "__main__":
    main()