END = (1<<19) - 1

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.value = 0

def build(left, right):
    node = Node()
    if left == right:
        return node
    mid = (left + right) // 2
    node.left = build(left, mid)
    node.right = build(mid + 1, right)
    return node

root = [build(0, END)]

def update(x):
    root.append(_update(root[-1], 0, END, x))

def _update(node, left, right, x):
    if x < left or x > right:
        return node
    new_node = Node()
    if left == right:
        new_node.value = node.weight + 1
        return new_node
    mid = (left + right) // 2
    new_node.left = _update(node.left, left, mid, x)
    new_node.right = _update(node.right, mid + 1, right, x)
    new_node.value = new_node.left.value + new_node.right.value
    return new_node

def query(version, left, right):
    return _query(root[version], 0, END, left, right)

def _query(node, left, right, ql, qr):
    if qr < left or right < ql:
        return 0
    if ql <= left and right <= qr:
        return node.weight
    mid = (left + right) // 2
    return _query(node.left, left, mid, ql, qr) + _query(node.right, mid + 1, right, ql, qr)

def delete(x):
    for _ in range(x):
        root.pop()

def count(node):
    return node.weight if node else 0

def xor(left, right, x):
    now_l = root[left - 1] if left > 0 else root[0]
    now_r = root[right]
    l, r = 0, END
    for i in range(18, -1, -1):  # 19비트
        bit = (x >> i) & 1
        mid = (l + r) // 2
        if bit == 0:
            if count(now_r.right) - count(now_l.right) > 0:
                now_l = now_l.right
                now_r = now_r.right
                l = mid + 1
            else:
                now_l = now_l.left
                now_r = now_r.left
                r = mid
        else:
            if count(now_r.left) - count(now_l.left) > 0:
                now_l = now_l.left
                now_r = now_r.left
                r = mid
            else:
                now_l = now_l.right
                now_r = now_r.right
                l = mid + 1
    return l

def _kth(left_root, right_root, left, right, k):
    if left == right:
        return left
    mid = (left + right) // 2
    left_count = count(right_root.left) - count(left_root.left)
    if k <= left_count:
        return _kth(left_root.left, right_root.left, left, mid, k)
    else:
        return _kth(left_root.right, right_root.right, mid + 1, right, k - left_count)


def kth(left,right,k):
    return _kth(root[left - 1], root[right], 0, END, k)


M = int(input())
result = []
for _ in range(M):
    cmd, *args = map(int, input().split())
    if cmd == 1:
        update(args[0])
    elif cmd == 2:
        result.append(xor(args[0], args[1], args[2]))
    elif cmd == 3:
        delete(args[0])
    elif cmd == 4:
        result.append(query(args[1], 0, args[2]) - query(args[0] - 1, 0, args[2]))
    elif cmd == 5:
        result.append(kth(args[0],args[1],args[2]))

print("\n".join(map(str, result)))
