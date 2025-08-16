class LinkCutNode:
    def __init__(self, val=0):
        self.left = None
        self.right = None
        self.parent = None
        self.path_parent = None
        self.rev = False
        self.val = val
        self.maxvalue = val
        self.sum = val
        self.size = 1

    def _is_root(self):
        return not self.parent or (self.parent.left is not self and self.parent.right is not self)

    def _update(self):
        self.sum = self.val
        self.size = 1
        self.maxvalue = self.val
        if self.left:
            self.sum += self.left.sum
            self.size += self.left.size
            self.maxvalue = max(self.left.maxvalue, self.maxvalue)
        if self.right:
            self.sum += self.right.sum
            self.size += self.right.size
            self.maxvalue = max(self.right.maxvalue, self.maxvalue)

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
                x.right.path_parent = x
                x.right.parent = None
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
        if self.find_root() is other.find_root():
            return
        self.path_parent = other

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

    def query(self, other):
        self.make_root()
        other.access()
        return other.sum

    def update(self, value):
        self.access()
        self.val = value
        self._update()

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

    def get_depth(self):
        self.access()
        if self.left:
            return self.left.size
        return 0

    def get_LCA(self, other):
        if not self.connected(other):
            return None
        self.access()
        last = other.access()
        self.splay()
        if self == last:
            return self
        return last

    def _find_max_node(self):
        target_max = self.maxvalue
        node = self
        while True:
            node._push()
            if node.left and node.left.maxvalue == target_max:
                node = node.left
            elif node.val == target_max:
                node.splay()
                return node
            else:
                node = node.right

    def query_max(self,other):
        self.make_root()
        other.access()
        return other.maxvalue

T = int(input())
for _ in range(T):
    n,m = map(int, input().split())
    vertices = [LinkCutNode(0) for i in range(n)]
    current_sum = 0
    for i in range(1, n):
        v,c = map(int, input().split())
        dummy = LinkCutNode(c)
        vertices[i].link(dummy)
        dummy.link(vertices[v])
        current_sum += c
    answer = 0
    for _ in range(m):
        u,v,w = map(int, input().split())
        u_node = vertices[u]
        v_node = vertices[v]
        if not u_node.connected(v_node):
            dummy = LinkCutNode(w)
            u_node.link(dummy)
            v_node.link(dummy)
            current_sum += w
        else:
            w_max = u_node.query_max(v_node)
            if w < w_max:
                v_node.access()
                heavy = v_node._find_max_node()
                if heavy:
                    heavy.splay()
                    if heavy.left:
                        heavy.left.parent = None
                        heavy.left = None
                    if heavy.right:
                        heavy.right.parent = None
                        heavy.right = None
                    heavy.parent = None
                    heavy.path_parent = None
                    heavy._update()
                    current_sum -= w_max
                    dummy = LinkCutNode(w)
                    u_node.link(dummy)
                    v_node.link(dummy)
                    current_sum += w
        answer ^= current_sum
    print(answer)