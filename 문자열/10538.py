import sys
from collections import deque

hp, wp, hm, wm = map(int, sys.stdin.readline().split())
pic   = [sys.stdin.readline().strip() for _ in range(hp)]
board = [sys.stdin.readline().strip() for _ in range(hm)]

conv  = {'x': 0, 'o': 1}
ncol  = wm - wp + 1
MASK  = (1 << hp) - 1
FULL  = 1 << (hp - 1)          # hp번째 비트

class Node:
    def __init__(self):
        self.child = [None, None]
        self.fail  = None
        self.out   = 0

root = Node()

def insert(row, idx):
    node = root
    for ch in row:
        k = conv[ch]
        if node.child[k] is None:
            node.child[k] = Node()
        node = node.child[k]
    node.out |= 1 << idx

for i, row in enumerate(pic):
    insert(row, i)

def build():
    q = deque()
    root.fail = root
    for k in range(2):
        if root.child[k]:
            root.child[k].fail = root
            q.append(root.child[k])
        else:
            root.child[k] = root
    while q:
        v = q.popleft()
        for k in range(2):
            u = v.child[k]
            if u:
                u.fail = v.fail.child[k]
                u.result |= u.fail.result
                q.append(u)
            else:
                v.child[k] = v.fail.child[k]

build()

state = [0] * ncol
ans   = 0

for r in range(hm):
    node = root
    for c in range(wm):
        node = node.child[conv[board[r][c]]]
        if c >= wp - 1:
            s = c - wp + 1
            state[s] = (((state[s] << 1) | 1) & node.out) & MASK
            if state[s] & FULL:
                ans += 1

print(ans)
