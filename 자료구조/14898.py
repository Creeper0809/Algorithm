import sys

class PersistentSegmentTree:
    class Node:
        def __init__(self, value=0, left=None, right=None):
            self.value = value
            self.left = left
            self.right = right

    def __init__(self, arr):
        self.n = len(arr)
        self.versions = []
        self.EMPTY_NODE = self.Node()
        self.EMPTY_NODE.left = self.EMPTY_NODE
        self.EMPTY_NODE.right = self.EMPTY_NODE

        root = self._build(arr, 0, self.n - 1)
        self.versions.append(root)

    def _build(self, arr, left, right):
        if left == right:
            return self.Node(value=arr[left])
        mid = (left + right) // 2
        left_child = self._build(arr, left, mid)
        right_child = self._build(arr, mid + 1, right)
        return self.Node(value=left_child.value + right_child.value, left=left_child, right=right_child)

    def update(self, version_idx, idx, delta):
        prev_root = self.versions[version_idx]
        new_root = self._update(prev_root, 0, self.n - 1, idx, delta)
        self.versions.append(new_root)
        return len(self.versions) - 1

    def _update(self, prev_node, left, right, idx, delta):
        if left == right:
            return self.Node(value=prev_node.value + delta)

        mid = (left + right) // 2
        left_child, right_child = prev_node.left, prev_node.right

        if idx <= mid:
            left_child = self._update(prev_node.left, left, mid, idx, delta)
        else:
            right_child = self._update(prev_node.right, mid + 1, right, idx, delta)

        return self.Node(value=left_child.value + right_child.value, left=left_child, right=right_child)

    def query(self, version_idx, query_left, query_right):
        if version_idx < 0 or version_idx >= len(self.versions):
            return 0
        root = self.versions[version_idx]
        return self._query(root, 0, self.n - 1, query_left, query_right)

    def _query(self, node, left, right, query_left, query_right):
        if query_left > right or query_right < left or node is self.EMPTY_NODE:
            return 0
        if query_left <= left and right <= query_right:
            return node.value
        mid = (left + right) // 2
        return self._query(node.left, left, mid, query_left, query_right) + self._query(node.right, mid + 1, right,
                                                                                        query_left, query_right)


def solve():
    sys.setrecursionlimit(2000005)
    input = sys.stdin.readline
    N = int(input())
    A = [0] + list(map(int, input().split()))
    unique_vals = sorted(list(set(A[1:])))
    compress = {val: i for i, val in enumerate(unique_vals, 1)}
    for i in range(1, N + 1):
        A[i] = compress[A[i]]
    prev_idx = [0] * (N + 1)
    max_compressed_val = len(unique_vals)
    last_seen = [0] * (max_compressed_val + 1)
    for i in range(1, N + 1):
        prev_idx[i] = last_seen[A[i]]
        last_seen[A[i]] = i
    pst = PersistentSegmentTree([0] * (N + 1))
    for i in range(1, N + 1):
        pst.update(i - 1, prev_idx[i], 1)
    Q = int(input())
    last_ans = 0
    for _ in range(Q):
        x, r = map(int, input().split())
        l = x + last_ans
        version_r = r
        version_l_minus_1 = l - 1
        ans = pst.query(version_r, 0, l - 1) - pst.query(version_l_minus_1, 0, l - 1)
        print(ans)
        last_ans = ans
solve()