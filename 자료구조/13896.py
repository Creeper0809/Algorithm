import sys
sys.setrecursionlimit(10 ** 6)
input = sys.stdin.readline

class LinkCutNode:
    def __init__(self, val=1):
        self.left = None
        self.right = None
        self.parent = None
        self.path_parent = None
        self.rev = False
        self.val = val
        self.size = val
        self.vir = 0

    def _is_root(self):
        return not self.parent or (self.parent.left is not self and self.parent.right is not self)

    def _update(self):
        self.size = self.val + self.vir
        if self.left:
            self.size += self.left.size
        if self.right:
            self.size += self.right.size

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
        g = p.parent
        if not p._is_root():
            if g.left is p:
                g.left = self
            else:
                g.right = self
        self.parent = g
        if p.left is self:
            p.left = self.right
            if self.right:
                self.right.parent = p
            self.right = p
        else:
            p.right = self.left
            if self.left:
                self.left.parent = p
            self.left = p
        p.parent = self
        self.path_parent = p.path_parent
        p.path_parent = None
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
            g = p.parent
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
            if x.right:
                x.vir += x.right.size
                x.right.path_parent = x
                x.right.parent = None
            if last:
                x.vir -= last.size
            x.right = last
            if last:
                last.parent = x
            x._update()
            last = x
            x = x.path_parent
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
        other.access()
        other.splay()
        self.path_parent = other
        other.vir += self.size
        other._update()

    def cut_parent(self):
        parent = self.get_parent()
        if not parent:
            return
        self.access()
        if self.left:
            self.left.parent = None
            self.left = None
            self._update()

    def cut(self, other):
        self.make_root()
        other.access()
        if other.left is self and not self.right:
            other.left.parent = None
            other.left = None
            other._update()

    def get_parent(self):
        self.access()
        if not self.left:
            return None
        parent = self.left
        parent._push()
        while parent.right:
            parent = parent.right
            parent._push()
        parent.splay()
        return parent


T = int(input())

for case in range(1, T + 1):
    print(f"Case #{case}:")

    N,Q,R = map(int, input().split())

    graph = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        a,b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    nodes = [None] + [LinkCutNode(1) for _ in range(1, N + 1)]


    def dfs(u, parent):
        for v in graph[u]:
            if v != parent:
                nodes[v].link(nodes[u])
                dfs(v, u)


    dfs(1, -1)

    current_root = nodes[R]
    current_root.make_root()

    for _ in range(Q):
        S,U = map(int, input().split())
        if S == 0:
            current_root = nodes[U]
            current_root.make_root()
        else:
            u_node = nodes[U]
            p = u_node.get_parent()
            u_node.cut_parent()
            ans = u_node.size
            if p:
                u_node.link(p)
            print(ans)