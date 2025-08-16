from collections import deque
import sys

L, C, W = map(int, sys.stdin.readline().split())
board = [sys.stdin.readline().strip() for _ in range(L)]
patterns = [sys.stdin.readline().strip() for _ in range(W)]

directions = [(-1, 0), (-1, 1), (0, 1), (1, 1)]
letter_dir = ["A", "B", "C", "D", "E", "F", "G", "H"]
alph = lambda ch: ord(ch) - 65

class Node:
    __slots__ = ("children", "fail", "output")
    def __init__(self):
        self.children = [None] * 26
        self.fail = None
        self.output = []

root = Node()

def insert(word, original, rev):
    node = root
    for ch in word:
        i = alph(ch)
        if node.children[i] is None:
            node.children[i] = Node()
        node = node.children[i]
    node.output.append((original, rev))

for p in patterns:
    insert(p, p, False)
    insert(p[::-1], p, True)

def build():
    q = deque()
    root.fail = root
    for i in range(26):
        if root.children[i]:
            root.children[i].fail = root
            q.append(root.children[i])
        else:
            root.children[i] = root
    while q:
        cur = q.popleft()
        for i in range(26):
            nxt = cur.ch[i]
            if nxt:
                nxt.fail = cur.fail.ch[i]
                nxt.output += nxt.fail.output
                q.append(nxt)
            else:
                cur.ch[i] = cur.fail.ch[i]

build()

def search_2d():
    res = {}
    N, M = len(board), len(board[0])
    for idx, (dx, dy) in enumerate(directions):
        if dx == 0 and dy == 1:
            starts = [(i, 0) for i in range(N)]
        elif dx == 1 and dy == 0:
            starts = [(0, j) for j in range(M)]
        elif dx == -1 and dy == 0:
            starts = [(N - 1, j) for j in range(M)]
        elif dx == -1 and dy == 1:
            starts = [(N - 1, j) for j in range(M)] + [(i, 0) for i in range(N - 1)]
        else:
            starts = [(0, j) for j in range(M)] + [(i, 0) for i in range(1, N)]
        for x0, y0 in starts:
            x, y, node = x0, y0, root
            while 0 <= x < N and 0 <= y < M:
                node = node.children[alph(board[x][y])]
                for pat, rev in node.output:
                    Lp = len(pat)
                    if not rev:
                        px = x - (Lp - 1) * dx
                        py = y - (Lp - 1) * dy
                        dch = letter_dir[idx]
                    else:
                        px = x
                        py = y
                        dch = letter_dir[idx + 4]
                    if 0 <= px < N and 0 <= py < M:
                        cand = (px, py, dch)
                        if pat not in res or cand < res[pat]:
                            res[pat] = cand
                x += dx
                y += dy
    return res

matches = search_2d()

for p in patterns:
    x, y, d = matches[p]
    print(f"{x} {y} {d}")
