import sys

sys.setrecursionlimit(1 << 25)


class LinkCutNode:
    def __init__(self, val=0):
        self.left = None
        self.right = None
        self.parent = None
        self.rev = False
        self.val = val
        self.mx = val

    def _is_root(self):
        return not self.parent or (self.parent.left is not self and self.parent.right is not self)

    def _update(self):
        self.mx = self.val
        if self.left and self.left.mx > self.mx:
            self.mx = self.left.mx
        if self.right and self.right.mx > self.mx:
            self.mx = self.right.mx

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
        stack = []
        node = self
        while True:
            stack.append(node)
            if node._is_root():
                break
            node = node.parent
        for n in reversed(stack):
            n._push()
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
        last = None
        x = self
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
        return other.mx

    def update(self, value):
        self.access()
        self.val = value
        self._update()


input = sys.stdin.readline
n = int(input())
nodes = [LinkCutNode(0) for _ in range(n + 1)]
edge_nodes = [None] * n
for i in range(1, n):
    u, v, w = map(int, input().split())
    e = LinkCutNode(w)
    edge_nodes[i] = e
    nodes[u].link(e)
    nodes[v].link(e)
q = int(input())
out = []
for _ in range(q):
    t, *rest = input().split()
    if t == '1':
        i, c = map(int, rest)
        edge_nodes[i].update(c)
    else:
        u, v = map(int, rest)
        out.append(str(nodes[u].query(nodes[v])))
sys.stdout.write('\n'.join(out))
