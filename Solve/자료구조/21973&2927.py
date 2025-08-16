import sys

sys.setrecursionlimit(200000)
input = sys.stdin.readline


class LinkCutNode:
    def __init__(self, val=0):
        self.left = self.right = self.parent = None
        self.rev = False
        self.val = val
        self.sum = val

    def _is_root(self):
        return not self.parent or (self.parent.left is not self and self.parent.right is not self)

    def _update(self):
        self.sum = self.val
        if self.left:
            self.sum += self.left.sum
        if self.right:
            self.sum += self.right.sum

    def _push(self):
        if self.rev:
            self.left, self.right = self.right, self.left
            if self.left:
                self.left.rev ^= True
            if self.right:
                self.right.rev ^= True
            self.rev = False

    def _rotate(self):
        p = self.parent
        g = p.p
        if not p._is_root():
            if g.left is p:
                g.left = self
            else:
                g.right = self
        self.parent = g
        if p.left is self:
            p.left = self.right
            if self.right:
                self.right.p = p
            self.right = p
        else:
            p.right = self.left
            if self.left:
                self.left.p = p
            self.left = p
        p.p = self
        p._update()
        self._update()

    def splay(self):
        stk, node = [], self
        while True:
            stk.append(node)
            if node._is_root():
                break
            node = node.parent
        for x in reversed(stk):
            x._push()
        while not self._is_root():
            p = self.parent
            g = p.p
            if not p._is_root():
                if (p.left is self) == (g.left is p):
                    p._rotate()
                else:
                    self._rotate()
            self._rotate()

    def access(self):
        last, x = None, self
        while x:
            x.splay()
            x.right = last
            x._update()
            last = x
            x = x.parent
        self.splay()
        return last

    def make_root(self):
        self.access()
        self.rev ^= True
        self._push()

    def find_root(self):
        self.access()
        x = self
        while True:
            x._push()
            if x.left:
                x = x.left
            else:
                break
        x.splay()
        return x

    def connected(self, other):
        return self.find_root() is other.find_root()

    def link(self, other):
        self.make_root()
        if self.find_root() is not other.find_root():
            self.parent = other
            return True
        return False

    def cut(self, other):
        self.make_root()
        other.access()
        if other.left is self and not self.right:
            other.left.p = None
            other.left = None
            other._update()

    def query(self, other):
        self.make_root()
        other.access()
        return other.sum

    def update(self, value):
        self.access()
        self.val = value
        self._update()


n = int(input())
vals = list(map(int, input().split()))
nodes = [None] + [LinkCutNode(v) for v in vals]
q = int(input())

out = sys.stdout
for _ in range(q):
    s = input().split()
    if s[0] == "bridge":
        a, b = map(int, s[1:])
        res = "yes" if nodes[a].link(nodes[b]) else "no"
        out.write(res + "\n")
        out.flush()
    elif s[0] == "penguins":
        a, x = map(int, s[1:])
        nodes[a].update(x)
    else:
        a, b = map(int, s[1:])
        if nodes[a].connected(nodes[b]):
            out.write(str(nodes[a].query(nodes[b])) + "\n")
        else:
            out.write("impossible\n")
        out.flush()
