import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

MOD = 10 ** 9 + 7

def build():
    for i in range(N):
        tree[size + i] = A[i] % MOD
    for i in range(size - 1, 0, -1):
        tree[i] = (tree[i << 1] + tree[i << 1 | 1]) % MOD


def push(node, l, r):
    if set_lazy[node] is not None:
        tree[node] = (set_lazy[node] * (r - l + 1)) % MOD
        if node < size:
            set_lazy[node << 1] = set_lazy[node << 1 | 1] = set_lazy[node]
            add_lazy[node << 1] = add_lazy[node << 1 | 1] = 0
            mul_lazy[node << 1] = mul_lazy[node << 1 | 1] = 1
        set_lazy[node] = None

    if mul_lazy[node] != 1 or add_lazy[node] != 0:
        tree[node] = (tree[node] * mul_lazy[node] + add_lazy[node] * (r - l + 1)) % MOD
        if node < size:
            for child in [node << 1, node << 1 | 1]:
                mul_lazy[child] = (mul_lazy[child] * mul_lazy[node]) % MOD
                add_lazy[child] = (add_lazy[child] * mul_lazy[node] + add_lazy[node]) % MOD
        mul_lazy[node] = 1
        add_lazy[node] = 0


def update(l, r, typ, val, node=1, nl=0, nr=None):
    if nr is None:
        nr = size - 1
    push(node, nl, nr)
    if r < nl or nr < l:
        return
    if l <= nl and nr <= r:
        if typ == 1:  # 덧셈
            add_lazy[node] = (add_lazy[node] + val) % MOD
        elif typ == 2:  # 곱셈
            mul_lazy[node] = (mul_lazy[node] * val) % MOD
            add_lazy[node] = (add_lazy[node] * val) % MOD
        elif typ == 3:  # 대입
            set_lazy[node] = val
            add_lazy[node] = 0
            mul_lazy[node] = 1
        push(node, nl, nr)
        return
    mid = (nl + nr) >> 1
    update(l, r, typ, val, node << 1, nl, mid)
    update(l, r, typ, val, node << 1 | 1, mid + 1, nr)
    tree[node] = (tree[node << 1] + tree[node << 1 | 1]) % MOD


def query(l, r, node=1, nl=0, nr=None):
    if nr is None:
        nr = size - 1
    push(node, nl, nr)
    if r < nl or nr < l:
        return 0
    if l <= nl and nr <= r:
        return tree[node]
    mid = (nl + nr) >> 1
    left = query(l, r, node << 1, nl, mid)
    right = query(l, r, node << 1 | 1, mid + 1, nr)
    return (left + right) % MOD

N = int(input())
A = list(map(int, input().split()))
M = int(input())

size = 1
while size < N:
    size <<= 1

tree = [0] * (2 * size)
add_lazy = [0] * (2 * size)
mul_lazy = [1] * (2 * size)
set_lazy = [None] * (2 * size)

build()

for _ in range(M):
    q = list(map(int, input().split()))
    if q[0] == 4:
        _, x, y = q
        print(query(x - 1, y - 1))
    else:
        t, x, y, v = q
        update(x - 1, y - 1, t, v)
