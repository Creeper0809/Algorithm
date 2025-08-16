import sys

input = sys.stdin.readline


class LinkCutNode:
    def __init__(self, val=0):
        self.left = None
        self.right = None
        self.parent = None
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
        return other.sum

    def update(self, value):
        self.access()
        self.val = value
        self._update()


def lca(u, v):
    u.access()
    return v.access()


n, q = map(int, input().split())
nodes = [LinkCutNode(i) for i in range(n + 1)]
result = []
for _ in range(q):
    t, *args = map(int, input().split())
    if t == 1:
        u, v = args
        nodes[u].link(nodes[v])
    elif t == 2:
        v = args[0]
        x = nodes[v]
        x.access()
        if x.left:
            x.left.p = None
            x.left = None
            x._update()
    else:
        u, v = args
        ancestor = lca(nodes[u], nodes[v])
        result.append(str(ancestor.val))
print('\n'.join(result))
