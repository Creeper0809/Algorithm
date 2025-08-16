from typing import List, Optional
from enum import Enum
import sys
sys.setrecursionlimit(int(1e9))

class Type(Enum):
    COMPRESS = 'Compress'
    RAKE = 'Rake'
    EDGE = 'Edge'

class Info:
    def __init__(self, sum_value=0, size_value=0):
        self.sum = sum_value
        self.size = size_value

class Node:
    def __init__(self, id):
        self.vs: List[Optional['Vertex']] = [None, None]
        self.dat: Optional['Cluster'] = None
        self.p: Optional['Node'] = None
        self.q: Optional['Node'] = None
        self.ch: List[Optional['Node']] = [None, None]
        self.rev: bool = False
        self.guard: bool = False
        self.type: Optional[Type] = None
        self.id = id
        self.path_lazy = 0
        self.subtree_lazy = 0

    def __str__(self):
        return "Node"+str(self.id)

    def debug(self):
        if self.type == Type.EDGE:
            print(f"Type: {self.type}, "
                  f"id: {self.id}, "
                  f"vs[0].id: {self.vs[0].id if self.vs[0] else 'None'}, vs[1].id: {self.vs[1].id if self.vs[1] else 'None'}, "
                  f"vs[0].value {self.vs[0].value if self.vs[0] else 'None}, "'}, vs[1].value: {self.vs[1].value if self.vs[1] else 'None},'} "
                  f"dat.path.sum: {self.dat.path.sum if self.dat else 'None'},"
                  ,end="")
            return
        print(f"Type: {self.type}, "
              f"id: {self.id}, "
              f"vs[0].id: {self.vs[0].id if self.vs[0] else 'None'}, vs[1].id: {self.vs[1].id if self.vs[1] else 'None'}, "
              f"dat.path.sum: {self.dat.path.sum if self.dat else 'None'},"
              #f"dat.subtree.sum: {self.dat.subtree.sum if self.dat else 'None'}, "
              f"dat.path.size: {self.dat.path.size if self.dat else 'None'},"
              #f"dat.subtree.size: {self.dat.subtree.size if self.dat else 'None'}, "
              f"path_lazy: {self.path_lazy},"
              #f"subtree_lazy: {self.subtree_lazy}, "
              #f"parent: {self.p if self.p else 'None'}, "
              f"child: left - {self.ch[0] if self.ch[0] else 'None'}, "
              f"right - {self.ch[1] if self.ch[1] else 'None'}, "
              f"rake - {self.q if self.q else 'None'}, ", end="")


class Vertex:
    def __init__(self, id=-1, value=0):
        self.value = value
        self.handle = None
        self.dummy = None
        self.id = id
        self.edge = None

    def __str__(self):
        return "Vertex: "+str(self.id)

class Cluster:
    def __init__(self, path_sum=0, subtree_sum=0, path_size=0, subtree_size=0):
        self.path = Info(path_sum, path_size)
        self.subtree = Info(subtree_sum, subtree_size)

    def __str__(self):
        return f"path.sum(size): {self.path.sum}({self.path.size}), subtree.sum(size): {self.subtree.sum}({self.subtree.size})"

    @staticmethod
    def rake(l: 'Cluster', vertex: 'Vertex', r: 'Cluster'):
        c = Cluster()
        c.path.sum = l.path.sum
        c.subtree.sum = l.subtree.sum + r.subtree.sum - vertex.value
        c.path.size = l.path.size
        c.subtree.size = l.subtree.size + r.subtree.size - (1 if vertex.id > 0 else 0)
        return c

    @staticmethod
    def compress(lf: 'Cluster', vertex: 'Vertex', r: 'Cluster'):
        c = Cluster()
        c.path.sum = lf.path.sum + r.path.sum - vertex.value
        c.subtree.sum = lf.subtree.sum + r.subtree.sum - vertex.value
        c.path.size = lf.path.size + r.path.size - (1 if vertex.id > 0 else 0)
        c.subtree.size = lf.subtree.size + r.subtree.size - (1 if vertex.id > 0 else 0)
        return c

    def toggle(self):
        pass

class TopTree:

    def __init__(self, N: int = 100000):
        self.N = N
        self.pool_vertex = [Vertex() for _ in range(2 * self.N)]
        self.ptr_vertex = 0
        self.pool_node = [Node(i) for i in range(4 * self.N)]
        self.ptr_node = 0
        self.id = Cluster(0)
        self.recycle: Optional[Node] = None
        self.root = None

    def create(self, id=-1, value=0):
        t = self.pool_vertex[self.ptr_vertex]
        self.ptr_vertex += 1
        t.__init__(id=id, value=value)
        dummy = self.pool_vertex[self.ptr_vertex]
        self.ptr_vertex += 1
        dummy.__init__(-id, 0)
        edge = self.link(t, self.id, dummy)
        t.edge = edge
        t.dummy = dummy
        return t

    def dispose_node(self, t: Node):
        t.p = self.recycle
        self.recycle = t

    def get_new_node(self) -> Node:
        if self.recycle:
            t = self.recycle
            self.recycle = self.recycle.p
            t.__init__(-1)
            return t
        t = self.pool_node[self.ptr_node]
        t.__init__(self.ptr_node)
        self.ptr_node += 1
        return t

    def edge(self, u: Vertex, w: Cluster, v: Vertex) -> Node:
        t = self.get_new_node()
        t.vs[0] = u
        t.vs[1] = v
        path_sum = u.value + w.path.sum + v.value
        subtree_sum = u.value + w.subtree.sum + v.value
        path_size = (1 if u.id > 0 else 0) + w.path.size + (1 if v.id > 0 else 0)
        subtree_size = (1 if u.id > 0 else 0) + w.subtree.size + (1 if v.id > 0 else 0)
        t.dat = Cluster(path_sum, subtree_sum, path_size, subtree_size)
        t.type = Type.EDGE
        return self.pushup(t)

    def compress(self, l: Node, r: Node) -> Node:
        t = self.get_new_node()
        t.ch[0] = l
        t.ch[1] = r
        t.type = Type.COMPRESS
        return self.pushup(t)

    def rake(self, l: Node, r: Node) -> Node:
        t = self.get_new_node()
        t.ch[0] = l
        t.ch[1] = r
        t.type = Type.RAKE
        return self.pushup(t)

    def make_root(self, v: Vertex):
        self.expose_vertex(v)
        self.root = v

    def parent_dir(self, t: Node) -> int:
        p = t.p
        if not p:
            return -1
        if p.guard:
            return -1
        if p.ch[0] == t:
            return 0
        if p.ch[1] == t:
            return 1
        return -1

    def parent_dir_ignore_guard(self, t: Node) -> int:
        p = t.p
        if not p:
            return -1
        if p.ch[0] == t:
            return 0
        if p.ch[1] == t:
            return 1
        return -1

    def pushup(self, t):
        print("-" * 20, f"Pushup start for node {t.id}", "-" * 20)
        t.debug()
        print("")
        l = t.ch[0]
        r = t.ch[1]

        if l:
            self.propagate(l)
        if r:
            self.propagate(r)
        if t.q:
            self.propagate(t.q)

        if t.type == Type.COMPRESS:
            assert l.vs[1] == r.vs[0]
            t.vs[0] = l.vs[0]
            t.vs[1] = r.vs[1]
            self.pushdown(r.vs[1].edge)

            if l.type == Type.EDGE:
                if abs(l.vs[0].id) != abs(l.vs[1].id):
                    sums = l.vs[0].val + l.vs[1].val
                    size = 2
                    l.dat = Cluster(path_sum=sums, subtree_sum=sums, path_size=size, subtree_size=size)

            if r.type == Type.EDGE:
                if abs(r.vs[0].id) != abs(r.vs[1].id):
                    sums = r.vs[0].val + r.vs[1].val
                    size = 2
                    r.dat = Cluster(path_sum=sums, subtree_sum=sums, path_size=size, subtree_size=size)

            lf = l.dat
            if t.q:
                assert l.vs[1] == t.q.vs[1]
                lf = Cluster.rake(l.dat, r.vs[0], t.q.dat)
            t.dat = Cluster.compress(lf, r.vs[0], r.dat)
            l.vs[1].handle = t

        if t.type == Type.EDGE:
            if abs(t.vs[0].id) != abs(t.vs[1].id):
                self.pushup(t.vs[0].edge)
                self.pushup(t.vs[1].edge)
                sums = t.vs[0].val + t.vs[1].val
                size = 2
                t.dat = Cluster(path_sum=sums, subtree_sum=sums, path_size=size, subtree_size=size)

        if t.type == Type.RAKE:
            assert l.vs[1] == r.vs[1]
            t.vs[0] = l.vs[0]
            t.vs[1] = l.vs[1]
            self.pushdown(r.vs[1].edge)
            t.dat = Cluster.rake(l.dat, r.vs[1], r.dat)
        else:
            if not t.p:
                t.vs[0].handle = t
                t.vs[1].handle = t
            elif t.p.type == Type.COMPRESS:
                if self.parent_dir(t) == -1:
                    t.vs[0].handle = t
            elif t.p.type == Type.RAKE:
                t.vs[0].handle = t
        print("-" * 20, f"Pushup end for node {t.id}", "-" * 20)
        t.debug()
        print("")
        return t

    def toggle(self, t: Node):
        if t.type == Type.EDGE:
            t.vs[0], t.vs[1] = t.vs[1], t.vs[0]
            t.dat.toggle()
        elif t.type == Type.COMPRESS:
            t.vs[0], t.vs[1] = t.vs[1], t.vs[0]
            t.dat.toggle()
            t.rev = not t.rev
        else:
            raise ValueError("Invalid type")

    def propagate(self, t: Node):
        if not t or not t.dat:
            return

        if t.rev and t.type == Type.COMPRESS:
            assert t.ch[0] and t.ch[1]
            t.ch[0], t.ch[1] = t.ch[1], t.ch[0]
            self.toggle(t.ch[0])
            self.toggle(t.ch[1])
            t.rev = False

        if t.subtree_lazy != 0:
            t.dat.path.sum += t.subtree_lazy * t.dat.path.size
            t.dat.subtree.sum += t.subtree_lazy * t.dat.subtree.size
            if t.type == Type.EDGE:
                if t.vs[0] and t.vs[0].id > 0: t.vs[0].value += t.subtree_lazy
                if t.vs[1] and t.vs[1].id > 0: t.vs[1].value += t.subtree_lazy
            else:
                if t.ch[0]: t.ch[0].subtree_lazy += t.subtree_lazy
                if t.ch[1]: t.ch[1].subtree_lazy += t.subtree_lazy
                if t.q: t.q.subtree_lazy += t.subtree_lazy

        if t.path_lazy != 0:
            t.dat.path.sum += t.path_lazy * t.dat.path.size
            t.dat.subtree.sum += t.path_lazy * t.dat.path.size
            if t.type == Type.EDGE and abs(t.vs[0].id) == abs(t.vs[1].id):
                if t.vs[0] and t.vs[0].id > 0: t.vs[0].value += t.path_lazy
                if t.vs[1] and t.vs[1].id > 0: t.vs[1].value += t.path_lazy
            elif t.type == Type.COMPRESS:
                if t.ch[0]: t.ch[0].path_lazy += t.path_lazy
                if t.ch[1]: t.ch[1].path_lazy += t.path_lazy
            elif t.type == Type.RAKE:
                if t.ch[0]: t.ch[0].path_lazy += t.path_lazy
        t.path_lazy = 0
        t.subtree_lazy = 0


    def set_toggle(self, v: Node):
        self.toggle(v)
        self.propagate(v)

    def pushdown(self, t: Optional[Node]):
        if not t:
            return
        self.pushdown(t.p)
        self.propagate(t)
        print("-"*20,f"Pushdown end for node {t.id}","-"*20)
        self.print_tree(t)

    def rotate(self, t: Node, x: Node, dir: int):
        y = x.p
        par = self.parent_dir_ignore_guard(x)
        self.propagate(t.ch[dir])
        x.ch[dir ^ 1] = t.ch[dir]
        t.ch[dir].p = x
        t.ch[dir] = x
        x.p = t
        t.p = y
        if par != -1:
            y.ch[par] = t
        elif y and y.type == Type.COMPRESS:
            y.q = t
        self.pushup(x)
        self.pushup(t)
        if y and not y.guard:
            self.pushup(y)

    def splay(self, t: Node):
        assert t.type != Type.EDGE
        self.propagate(t)

        while self.parent_dir(t) != -1:
            q = t.p
            if q.type != t.type:
                break
            if self.parent_dir(q) != -1 and q.p and q.p.type == q.type:
                r = q.p
                if r.p:
                    self.propagate(r.p)
                self.propagate(r)
                self.propagate(q)
                self.propagate(t)
                qt_dir = self.parent_dir(t)
                rq_dir = self.parent_dir(q)
                if rq_dir == qt_dir:
                    self.rotate(q, r, rq_dir ^ 1)
                    self.rotate(t, q, qt_dir ^ 1)
                else:
                    self.rotate(t, q, qt_dir ^ 1)
                    self.rotate(t, r, rq_dir ^ 1)
            else:
                if q.p:
                    self.propagate(q.p)
                self.propagate(q)
                self.propagate(t)
                qt_dir = self.parent_dir(t)
                self.rotate(t, q, qt_dir ^ 1)

    def expose(self, t: Node) -> Node:
        # print(f"Expose start for node {t.id}")
        self.pushdown(t)
        while True:
            assert t.type != Type.RAKE
            if t.type == Type.COMPRESS:
                self.splay(t)
            n = None
            p = t.p
            if not p:
                break
            if p.type == Type.RAKE:
                self.propagate(p)
                self.splay(p)
                n = p.p
            if p.type == Type.COMPRESS:
                self.propagate(p)
                if p.guard and self.parent_dir_ignore_guard(t) != -1:
                    break
                n = p

            self.splay(n)

            dir = self.parent_dir_ignore_guard(n)
            if dir == -1 or n.p.type == Type.RAKE:
                dir = 0

            c = n.ch[dir]
            if dir == 1:
                self.set_toggle(c)
                self.set_toggle(t)
            n_dir = self.parent_dir(t)
            if n_dir != -1:
                r = t.p
                self.propagate(c)
                self.propagate(r)
                r.ch[n_dir] = c
                c.p = r
                n.ch[dir] = t
                t.p = n
                self.pushup(c)
                self.pushup(r)
                self.pushup(t)
                self.pushup(n)
                self.splay(r)
            else:
                self.propagate(c)
                n.q = c
                c.p = n
                n.ch[dir] = t
                t.p = n
                self.pushup(c)
                self.pushup(t)
                self.pushup(n)
            if t.type == Type.EDGE:
                t = n
        # print(f"Expose end for node {t.id}")
        return t

    def expose_vertex(self, v: Vertex) -> Node:
        # print(f"Expose_vertex start for vertex {v.id}")
        t = self.expose(v.handle)
        # print(f"Expose_vertex end for vertex {v.id}, returning node {t.id}")
        return t

    def soft_expose(self, u: Vertex, v: Vertex):
        self.pushdown(u.handle)
        self.pushdown(v.handle)
        rt = self.expose_vertex(u)

        if u.handle == v.handle:
            if rt.vs[1] == u or rt.vs[0] == v:
                self.set_toggle(rt)
            return

        rt.guard = True
        soft = self.expose_vertex(v)
        rt.guard = False

        self.pushup(rt)
        if self.parent_dir(soft) == 0:
            self.set_toggle(rt)

    def bring(self, rt: Node):
        rk = rt.q
        if not rk:
            ll = rt.ch[0]
            self.dispose_node(ll.p)
            ll.p = None
            self.pushup(ll)
        elif rk.type in (Type.COMPRESS, Type.EDGE):
            nr = rk
            self.set_toggle(nr)
            rt.ch[1] = nr
            nr.p = rt
            rt.q = None

            self.pushup(nr)
            self.pushup(rt)
        elif rk.type == Type.RAKE:
            self.propagate(rk)
            while rk.ch[1].type == Type.RAKE:
                self.propagate(rk.ch[1])
                rk = rk.ch[1]
            self.pushdown(rk)

            rt.guard = True
            self.splay(rk)
            rt.guard = False

            ll = rk.ch[0]
            rr = rk.ch[1]
            self.propagate(ll)
            self.set_toggle(rr)

            rt.ch[1] = rr
            rr.p = rt

            rt.q = ll
            ll.p = rt

            self.dispose_node(rk)
            self.pushup(ll)
            self.pushup(rr)
            self.pushup(rt)

    def link(self, u: Vertex, w: Cluster, v: Vertex) -> Node:
        if u.id > v.id: u, v = v, u

        if not u.handle and not v.handle:
            return self.edge(u, w, v)

        nnu = u.handle
        nnv = v.handle
        ee = self.edge(u, w, v)
        ll = None

        assert nnv
        vv = self.expose(nnv)
        self.propagate(vv)
        if vv.vs[1] == v:
            self.set_toggle(vv)
        if vv.vs[0] == v:
            nv = self.compress(ee, vv)
            ee.p = nv
            self.pushup(ee)
            vv.p = nv
            self.pushup(vv)
            self.pushup(nv)
            ll = nv
        else:
            nv = vv
            ch = nv.ch[0]
            self.propagate(ch)
            nv.ch[0] = ee
            ee.p = nv
            self.pushup(ee)

            bt = nv.q
            rk = None
            if bt:
                self.propagate(bt)
                rk = self.rake(bt, ch)
                bt.p = rk
                ch.p = rk
                self.pushup(bt)
                self.pushup(ch)
            else:
                rk = ch
            nv.q = rk
            rk.p = nv
            self.pushup(rk)
            self.pushup(nv)
            ll = nv

        assert nnu
        uu = self.expose(nnu)
        self.propagate(uu)
        if uu.vs[0] == u:
            self.set_toggle(uu)
        if uu.vs[1] == u:
            tp = self.compress(uu, ll)
            uu.p = tp
            ll.p = tp
            self.pushup(uu)
            self.pushup(ll)
            self.pushup(tp)
        else:
            nu = uu
            ch = nu.ch[1]
            self.set_toggle(ch)

            nu.ch[1] = ll
            ll.p = nu
            self.pushup(ll)

            al = nu.q
            rk = None
            if al:
                self.propagate(al)
                rk = self.rake(al, ch)
                al.p = rk
                ch.p = rk
                self.pushup(al)
                self.pushup(ch)
            else:
                rk = ch
            nu.q = rk
            rk.p = nu
            self.pushup(rk)
            self.pushup(nu)

        return ee

    def cut(self, u: Vertex, v: Vertex):
        self.soft_expose(u, v)
        rt = u.handle
        self.propagate(rt)
        rr = rt.ch[1]
        rr.p = None
        self.set_toggle(rr)
        assert rr.ch[1].type == Type.EDGE
        self.dispose_node(rr.ch[1])
        self.bring(rr)
        self.bring(rt)

    def path(self, u, v):
        self.soft_expose(u, v)
        rt = self.expose_vertex(u)
        self.propagate(rt)
        if rt.type != Type.EDGE:
            self.propagate(rt.ch[1])
        return rt

    def set_vertex(self, u: Vertex, v: Vertex):
        t = self.expose_vertex(u)
        u.value = v.value
        self.pushup(t)

    def set_edge(self, u: Vertex, v: Vertex, w: Cluster):
        t = self.path(u, v)
        assert t.type == Type.EDGE
        t.dat.path.sum = t.vs[0].value + w.path.sum + t.vs[1].value
        t.dat.subtree.sum = t.vs[0].value + w.subtree.sum + t.vs[1].value
        while t:
            self.pushup(t)
            t = t.p

    def get_path(self, u: Vertex, v: Vertex) -> Info:
        if u == v:
            return Info(u.value)
        node = self.path(u.dummy, v.dummy)
        self.print_tree(node)
        return node.dat.path

    def get_subtree(self, root: Vertex, v: Vertex) -> Info:
        if root == v:
            t = self.expose_vertex(root)
            return t.dat.subtree
        self.soft_expose(v, root)
        t = self.expose_vertex(v)
        self.propagate(t)
        if t.type == Type.EDGE:
            return Info(v.value)
        lf = t.ch[0].dat
        if t.q:
            lf = Cluster.rake(t.ch[0].dat, t.ch[1].vs[0], t.q.dat)
        return lf.subtree

    def add_subtree(self, root: Vertex, v: Vertex, x: int):
        if root == v:
            t = self.expose_vertex(root)
            t.subtree_lazy += x
            self.pushdown(t)
            self.pushup(t)
            return
        self.soft_expose(v, root)
        t = self.expose_vertex(v)
        t.subtree_lazy += x
        self.pushdown(t)
        self.pushup(t)

    def add_path(self, u: Vertex, v: Vertex, x: int):
        t = self.path(u.dummy, v.dummy)

        t.path_lazy += x
        print(f"\npath added:",end="")
        t.debug()
        print("")

        self.print_tree(t)

    def get_included_vertices_in_subtree(self, node: Optional[Node]) -> List[int]:
        if not node:
            return []
        vertices = []
        if node.type == Type.EDGE:
            for v in node.vs:
                if v and v.id > 0:
                    vertices.append(v.id)
        elif node.type == Type.COMPRESS:
            vertices.extend(self.get_included_vertices_in_subtree(node.ch[0]))
            vertices.extend(self.get_included_vertices_in_subtree(node.ch[1]))
            if node.q:
                vertices.extend(self.get_included_vertices_in_subtree(node.q))
        elif node.type == Type.RAKE:
            vertices.extend(self.get_included_vertices_in_subtree(node.ch[0]))
            vertices.extend(self.get_included_vertices_in_subtree(node.ch[1]))
            if node.q:
                vertices.extend(self.get_included_vertices_in_subtree(node.q))
        return sorted(list(set(vertices)))

    def get_included_vertices_in_path(self, node: Optional[Node]) -> List[int]:
        if not node:
            return []
        vertices = []
        if node.type == Type.EDGE:
            for v in node.vs:
                if v:
                    vertices.append(v.id)
        elif node.type == Type.COMPRESS:
            vertices.extend(self.get_included_vertices_in_path(node.ch[0]))
            vertices.extend(self.get_included_vertices_in_path(node.ch[1]))
        elif node.type == Type.RAKE:
            vertices.extend(self.get_included_vertices_in_path(node.ch[0]))
            vertices.extend(self.get_included_vertices_in_path(node.ch[1]))
            if node.q:
                vertices.extend(self.get_included_vertices_in_path(node.q))
        return list(set(vertices))

    def print_tree(self, node=None):
        node = node or self.root
        if node is None:
            print("No tree")
            return

        def recurse(n, depth=0):
            if n is None:
                return
            print('--' * depth, end="")
            n.debug()
            # print(f"included verts(subtree): {self.get_included_vertices_in_subtree(n)}, ", end="")
            print(f"included verts(path): {self.get_included_vertices_in_path(n)}")

            recurse(n.ch[0], depth + 1)
            recurse(n.ch[1], depth + 1)
            if n.q:
                recurse(n.q, depth + 1)

        if isinstance(node, Vertex):
            node = node.handle
        recurse(node)
        print("")

def test():
    tt = TopTree()
    vertices = [None] + [tt.create(i, i) for i in range(1, 16)]

    # 복잡한 트리 구조 생성: 루트 1에 브랜치 여러 개, 깊은 체인 포함
    # 1 -- 2 -- 3 -- 4 -- 5 -- 6
    #   |     |
    #   |     -- 7 -- 8
    #   -- 9 -- 10 -- 11
    #   |
    #   -- 12 -- 13 -- 14 -- 15
    tt.link(vertices[1], Cluster(), vertices[2])
    tt.link(vertices[2], Cluster(), vertices[3])
    tt.link(vertices[3], Cluster(), vertices[4])
    tt.link(vertices[4], Cluster(), vertices[5])
    tt.link(vertices[5], Cluster(), vertices[6])
    tt.link(vertices[3], Cluster(), vertices[7])
    tt.link(vertices[7], Cluster(), vertices[8])
    tt.link(vertices[1], Cluster(), vertices[9])
    tt.link(vertices[9], Cluster(), vertices[10])
    tt.link(vertices[10], Cluster(), vertices[11])
    tt.link(vertices[1], Cluster(), vertices[12])
    tt.link(vertices[12], Cluster(), vertices[13])
    tt.link(vertices[13], Cluster(), vertices[14])
    tt.link(vertices[14], Cluster(), vertices[15])
    tt.make_root(vertices[1])
    # 초기 상태 검증
    print("--- Initial State Verification ---")
    # 경로 1-6 합: 1+2+3+4+5+6 = 21
    initial_path_1_6 = tt.get_path(vertices[1], vertices[6]).sum
    print(f"Initial path sum (1 to 6): {initial_path_1_6}")
    initial_path_6_1 = tt.get_path(vertices[1], vertices[6]).sum
    print(f"Initial path sum (1 to 6): {initial_path_6_1}")
    assert initial_path_1_6 == 21

    # 경로 3-8 합: 3+7+8 = 18
    initial_path_3_8 = tt.get_path(vertices[8], vertices[3]).sum
    print(f"Initial path sum (3 to 8): {initial_path_3_8}")
    assert initial_path_3_8 == 18

    # 경로 1-11 합: 1+9+10+11 = 31
    initial_path_1_11 = tt.get_path(vertices[11], vertices[1]).sum
    print(f"Initial path sum (1 to 11): {initial_path_1_11}")
    assert initial_path_1_11 == 31

    # 경로 12-15 합: 12+13+14+15 = 54
    initial_path_12_15 = tt.get_path(vertices[15], vertices[12]).sum
    print(f"Initial path sum (12 to 15): {initial_path_12_15}")
    assert initial_path_12_15 == 54
    print("Initial state OK.\n")

    # add_path 연산: 경로 1-6에 +2 (정점 1,2,3,4,5,6 영향)
    print("--- Path Update 1: add_path(1, 6, 2) ---")
    tt.add_path(vertices[1], vertices[6], 2)
    print("add_path(1, 6, 2) executed.")

    # # 경로 1-6 합: 21 + (2*6) = 33
    # path_1_6_after_add1 = tt.get_path(vertices[6], vertices[1]).sum
    # print(f"After update1, path sum (1 to 6): {path_1_6_after_add1}")
    # assert path_1_6_after_add1 == 33

    # 경로 3-8 합: 18 + (2*1) = 20 (3만 영향)
    path_3_8_after_add1 = tt.get_path(vertices[3], vertices[8]).sum
    print(f"After update1, path sum (3 to 8): {path_3_8_after_add1}")
    assert path_3_8_after_add1 == 20

    # 경로 1-11 합: 31 + (2*1) = 33 (1만 영향)
    path_1_11_after_add1 = tt.get_path(vertices[1], vertices[11]).sum
    print(f"After update1, path sum (1 to 11): {path_1_11_after_add1}")
    assert path_1_11_after_add1 == 33

    # 경로 12-15 합: 54 (변화 없음)
    path_12_15_after_add1 = tt.get_path(vertices[12], vertices[15]).sum
    print(f"After update1, path sum (12 to 15): {path_12_15_after_add1}")
    assert path_12_15_after_add1 == 54
    print("Path update 1 OK.\n")

    # add_path 연산: 경로 7-8에 +3 (정점 7,8 영향, 3-8 경로에 오버랩)
    print("--- Path Update 2: add_path(7, 8, 3) ---")
    tt.add_path(vertices[7], vertices[8], 3)
    print("add_path(7, 8, 3) executed.")

    # 경로 1-6 합: 33 (변화 없음, 브랜치 다름)
    path_1_6_after_add2 = tt.get_path(vertices[1], vertices[6]).sum
    print(f"After update2, path sum (1 to 6): {path_1_6_after_add2}")
    assert path_1_6_after_add2 == 33

    # 경로 3-8 합: 20 + (3*2) = 26 (7,8 영향)
    path_3_8_after_add2 = tt.get_path(vertices[3], vertices[8]).sum
    print(f"After update2, path sum (3 to 8): {path_3_8_after_add2}")
    assert path_3_8_after_add2 == 26

    # 경로 1-11 합: 33 (변화 없음)
    path_1_11_after_add2 = tt.get_path(vertices[1], vertices[11]).sum
    print(f"After update2, path sum (1 to 11): {path_1_11_after_add2}")
    assert path_1_11_after_add2 == 33
    print("Path update 2 OK.\n")

    # add_path 연산: 경로 1-15에 +1 (정점 1,12,13,14,15 영향)
    print("--- Path Update 3: add_path(1, 15, 1) ---")
    tt.add_path(vertices[1], vertices[15], 1)
    print("add_path(1, 15, 1) executed.")

    # 경로 1-6 합: 33 + (1*1) = 34 (1 영향)
    path_1_6_after_add3 = tt.get_path(vertices[1], vertices[6]).sum
    print(f"After update3, path sum (1 to 6): {path_1_6_after_add3}")
    assert path_1_6_after_add3 == 34

    # 경로 3-8 합: 26 (변화 없음)
    path_3_8_after_add3 = tt.get_path(vertices[3], vertices[8]).sum
    print(f"After update3, path sum (3 to 8): {path_3_8_after_add3}")
    assert path_3_8_after_add3 == 26

    # 경로 12-15 합: 54 + (1*4) = 58 (12~15 영향)
    path_12_15_after_add3 = tt.get_path(vertices[12], vertices[15]).sum
    print(f"After update3, path sum (12 to 15): {path_12_15_after_add3}")
    assert path_12_15_after_add3 == 58

    # 경로 1-15 합: (1+12+13+14+15) 초기 1+12+13+14+15=55 + 이전(1+2 from add1, but wait: 초기 55, add1 no, add2 no, add3 +1*5=60
    path_1_15_after_add3 = tt.get_path(vertices[1], vertices[15]).sum
    print(f"After update3, path sum (1 to 15): {path_1_15_after_add3}")
    assert path_1_15_after_add3 == 60
    print("Path update 3 OK.\n")

    # 최종 정점 값 확인
    print("--- Final Vertex Values ---")
    expected_values = {
        1: 1 + 2 + 1,  # add1 +2, add3 +1
        2: 2 + 2,
        3: 3 + 2,
        4: 4 + 2,
        5: 5 + 2,
        6: 6 + 2,
        7: 7 + 3,
        8: 8 + 3,
        9: 9,
        10: 10,
        11: 11,
        12: 12 + 1,
        13: 13 + 1,
        14: 14 + 1,
        15: 15 + 1
    }
    all_values_ok = True
    for i in range(1, 16):
        expected = expected_values[i]
        actual = vertices[i].value
        print(f"Vertex {i}: value = {actual} (expected: {expected})")
        if actual != expected:
            all_values_ok = False
    assert all_values_ok
    print("All final values OK.")
    print("\nAll tests passed!")

test()

# tt = TopTree()
#
# vertices = [None] + [tt.create(i, i) for i in range(1, 10)]
#
# tt.link(vertices[1], Cluster(), vertices[2])
# tt.link(vertices[1], Cluster(), vertices[3])
# tt.link(vertices[4], Cluster(), vertices[3])
# tt.link(vertices[3], Cluster(), vertices[5])
# tt.link(vertices[5], Cluster(), vertices[6])
# tt.link(vertices[5], Cluster(), vertices[7])
#
# tt.make_root(vertices[1])
# # print(tt.get_path(vertices[3], vertices[4]).sum)
# print("asd-" * 20)
# tt.add_path(vertices[1], vertices[3], 1)
# print(tt.get_path(vertices[3], vertices[4]).sum)
# print("-" * 20)