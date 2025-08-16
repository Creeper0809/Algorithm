import sys
sys.setrecursionlimit(10**6)

class Vertex:
    def __init__(self, id_val=0, weight_val=0):
        self.id = id_val
        self.weight = weight_val
        self.handle = None

class Cluster:
    def __init__(self, v=0, ws=0, sdl=0, sdr=0):
        self.value = v
        self.weight_sum = ws
        self.sum_dist_left = sdl
        self.sum_dist_right = sdr

    def toggle(self):
        self.sum_dist_left, self.sum_dist_right = self.sum_dist_right, self.sum_dist_left

    @staticmethod
    def compress(L, mid_vertex, R):
        mid_w = mid_vertex.weight
        L_val = L.value
        R_val = R.value
        L_ws = L.weight_sum
        R_ws = R.weight_sum
        return Cluster(
            L_val + R_val,
            L_ws + R_ws - mid_w,
            L.sum_dist_left + R.sum_dist_left + L_val * (R_ws - mid_w),
            L.sum_dist_right + R.sum_dist_right + R_val * (L_ws - mid_w)
        )

    @staticmethod
    def rake(path_part, shared_vertex, side_subtree):
        shared_w = shared_vertex.weight
        path_val = path_part.value
        side_ws = side_subtree.weight_sum
        return Cluster(
            path_val,
            path_part.weight_sum + side_ws - shared_w,
            path_part.sum_dist_left + side_subtree.sum_dist_right + path_val * (side_ws - shared_w),
            path_part.sum_dist_right + side_subtree.sum_dist_right
        )

class Type:
    COMPRESS = 0
    RAKE = 1
    EDGE = 2

class Node:
    def __init__(self):
        self.vs = [None, None]
        self.dat = Cluster()
        self.p = None
        self.q = None
        self.ch = [None, None]
        self.type = None
        self.rev = False
        self.guard = False

class TopTree:
    node_pool = [Node() for _ in range(2000000)]
    pool_idx = 0

    def __init__(self):
        self.id_cluster = Cluster(0)

    def alloc_node(self):
        if self.pool_idx >= 2000000:
            print("Node pool overflow!", file=sys.stderr)
            sys.exit(1)
        node = self.node_pool[self.pool_idx]
        self.pool_idx += 1
        return node

    def parent_dir(self, t):
        if not t or not t.p or t.p.guard:
            return -1
        p = t.p
        if p.ch[0] == t:
            return 0
        elif p.ch[1] == t:
            return 1
        return -1

    def parent_dir_ignore_guard(self, t):
        if not t or not t.p:
            return -1
        p = t.p
        if p.ch[0] == t:
            return 0
        elif p.ch[1] == t:
            return 1
        return -1

    def toggle(self, t):
        if t.type == Type.EDGE:
            t.vs[0], t.vs[1] = t.vs[1], t.vs[0]
            t.dat.toggle()
        elif t.type == Type.COMPRESS:
            t.vs[0], t.vs[1] = t.vs[1], t.vs[0]
            t.dat.toggle()
            t.rev = not t.rev

    def propagate(self, t):
        if not t or t.type != Type.COMPRESS or not t.rev:
            return
        l = t.ch[0]
        r = t.ch[1]
        t.ch[0], t.ch[1] = t.ch[1], t.ch[0]
        self.toggle(l)
        self.toggle(r)
        t.rev = False

    def pushup(self, t):
        if not t:
            return None
        self.propagate(t)
        l = t.ch[0]
        r = t.ch[1]

        if t.type == Type.EDGE:
            value = t.dat.value
            u = t.vs[0]
            v = t.vs[1]
            u_w = u.weight
            v_w = v.weight
            t.dat = Cluster(value, u_w + v_w, v_w * value, u_w * value)

        if t.type == Type.COMPRESS:
            self.propagate(l)
            self.propagate(r)
            t.vs[0] = l.vs[0]
            t.vs[1] = r.vs[1]
            lf = l.dat
            if t.q:
                self.propagate(t.q)
                lf = Cluster.rake(l.dat, l.vs[1], t.q.dat)
            t.dat = Cluster.compress(lf, r.vs[0], r.dat)
            l.vs[1].handle = t
        elif t.type == Type.RAKE:
            t.vs[0] = l.vs[0]
            t.vs[1] = l.vs[1]
            t.dat = Cluster.rake(l.dat, l.vs[1], r.dat)

        if t.type != Type.RAKE:
            if not t.p:
                t.vs[0].handle = t
                t.vs[1].handle = t
            elif t.p.type == Type.COMPRESS and self.parent_dir(t) == -1:
                t.vs[0].handle = t
            elif t.p.type == Type.RAKE:
                t.vs[0].handle = t
        return t

    def set_toggle(self, v):
        self.toggle(v)
        self.propagate(v)

    def pushdown(self, t):
        if not t:
            return
        path = []
        curr = t
        while curr:
            path.append(curr)
            curr = curr.p
        for node in reversed(path):
            self.propagate(node)

    def rotate(self, t, x, dir):
        y = x.p
        par = self.parent_dir_ignore_guard(x)

        x.ch[dir ^ 1] = t.ch[dir]
        if t.ch[dir]:
            t.ch[dir].p = x

        t.ch[dir] = x
        x.p = t
        t.p = y

        if par != -1:
            if y:
                y.ch[par] = t
        elif y and y.type == Type.COMPRESS:
            y.q = t

        self.pushup(x)
        self.pushup(t)
        if y and not y.guard:
            self.pushup(y)

    def splay(self, t):
        self.pushdown(t)
        while self.parent_dir(t) != -1:
            q = t.p
            if q.type != t.type:
                break
            if self.parent_dir(q) != -1 and q.p and q.p.type == q.type:
                r = q.p
                qt_dir = self.parent_dir(t)
                rq_dir = self.parent_dir(q)
                if rq_dir == qt_dir:
                    self.rotate(q, r, rq_dir ^ 1)
                    self.rotate(t, q, qt_dir ^ 1)
                else:
                    self.rotate(t, q, qt_dir ^ 1)
                    self.rotate(t, r, rq_dir ^ 1)
            else:
                qt_dir = self.parent_dir(t)
                self.rotate(t, q, qt_dir ^ 1)

    def expose(self, t):
        self.pushdown(t)
        while True:
            if t.type == Type.COMPRESS:
                self.splay(t)
            p = t.p
            if not p:
                break
            n = None
            if p.type == Type.RAKE:
                self.propagate(p)
                self.splay(p)
                n = p.p
            elif p.type == Type.COMPRESS:
                self.propagate(p)
                if p.guard and self.parent_dir_ignore_guard(t) != -1:
                    break
                n = p
            if not n:
                break
            self.splay(n)
            dir = self.parent_dir_ignore_guard(n)
            if dir == -1 or (n.p and n.p.type == Type.RAKE):
                dir = 0
            c = n.ch[dir]
            if dir == 1:
                self.set_toggle(c)
                self.set_toggle(t)
            n_dir = self.parent_dir(t)
            if n_dir != -1:
                r_node = t.p
                self.propagate(c)
                self.propagate(r_node)
                r_node.ch[n_dir] = c
                if c:
                    c.p = r_node
                n.ch[dir] = t
                t.p = n
                self.pushup(c)
                self.pushup(r_node)
                self.pushup(t)
                self.pushup(n)
                self.splay(r_node)
            else:
                self.propagate(c)
                n.q = c
                if c:
                    c.p = n
                n.ch[dir] = t
                t.p = n
                self.pushup(c)
                self.pushup(t)
                self.pushup(n)
            if t.type == Type.EDGE:
                t = n
        return t

    def recursive_pushup(self, t):
        if not t:
            return
        self.propagate(t)
        self.recursive_pushup(t.ch[0])
        self.recursive_pushup(t.ch[1])
        if t.type == Type.COMPRESS:
            self.recursive_pushup(t.q)
        self.pushup(t)

    def find_median_in_cluster(self, t, ext_W0, ext_W1):
        if not t:
            return None
        total_W = t.dat.weight_sum + ext_W0 + ext_W1
        half = total_W >> 1
        self.pushdown(t)

        if t.type == Type.EDGE:
            v0 = t.vs[0]
            v1 = t.vs[1]
            W_dir0 = ext_W0
            W_dir1 = v1.weight + ext_W1
            if max(W_dir0, W_dir1) <= half:
                return v0
            elif W_dir1 > half:
                return v1
            else:
                return v0
        elif t.type == Type.COMPRESS:
            l = t.ch[0]
            r = t.ch[1]
            q = t.q
            mid = r.vs[0]
            mid_w = mid.weight
            W_left = l.dat.weight_sum - mid_w + ext_W0
            W_right = r.dat.weight_sum - mid_w + ext_W1
            W_side = q.dat.weight_sum - mid_w if q else 0

            max_w = max(W_left, W_right, W_side)
            if max_w <= half:
                return mid
            if W_left == max_w:
                return self.find_median_in_cluster(l, ext_W0, W_right + W_side)
            elif W_right == max_w:
                return self.find_median_in_cluster(r, W_left + W_side, ext_W1)
            else:
                return self.find_median_in_cluster(q, 0, W_left + W_right)
        elif t.type == Type.RAKE:
            l = t.ch[0]
            r = t.ch[1]
            mid = t.vs[1]
            mid_w = mid.weight
            W_left = l.dat.weight_sum - mid_w + ext_W0
            W_side = r.dat.weight_sum - mid_w
            max_w = max(W_left, W_side, ext_W1)
            if max_w <= half:
                return mid
            if W_left == max_w:
                return self.find_median_in_cluster(l, ext_W0, W_side + ext_W1)
            elif W_side == max_w:
                return self.find_median_in_cluster(r, 0, W_left + ext_W1)
            else:
                return mid
        return None

    def create(self, id_val=0, weight=0):
        t = Vertex(id_val, weight)
        dummy = Vertex(0, 0)
        self.link(t, self.id_cluster, dummy)
        return t

    def edge(self, u, w, v):
        t = self.alloc_node()
        t.vs[0] = u
        t.vs[1] = v
        u_w = u.weight
        v_w = v.weight
        t.dat = Cluster(w.value, u_w + v_w, v_w * w.value, u_w * w.value)
        t.type = Type.EDGE
        return self.pushup(t)

    def compress(self, l, r):
        t = self.alloc_node()
        t.ch[0] = l
        t.ch[1] = r
        t.type = Type.COMPRESS
        l.p = t
        r.p = t
        return self.pushup(t)

    def rake(self, l, r):
        t = self.alloc_node()
        t.ch[0] = l
        t.ch[1] = r
        t.type = Type.RAKE
        l.p = t
        r.p = t
        return self.pushup(t)

    def expose_vertex(self, v):
        return self.expose(v.handle)

    def soft_expose(self, u, v):
        self.pushdown(u.handle)
        self.pushdown(v.handle)
        rt = self.expose(u.handle)

        if u.handle == v.handle:
            if rt.vs[1] == u or rt.vs[0] == v:
                self.set_toggle(rt)
            return

        rt.guard = True
        soft = self.expose(v.handle)
        rt.guard = False

        self.pushup(rt)
        if self.parent_dir(soft) == 0:
            self.set_toggle(rt)

    def bring(self, rt):
        rk = rt.q
        if not rk:
            ll = rt.ch[0]
            if ll:
                ll.p = None
            self.pushup(ll)
        elif rk.type == Type.COMPRESS or rk.type == Type.EDGE:
            nr = rk
            self.set_toggle(nr)
            rt.ch[1] = nr
            nr.p = rt
            rt.q = None
            self.pushup(nr)
            self.pushup(rt)
        elif rk.type == Type.RAKE:
            self.propagate(rk)
            while rk.ch[1] and rk.ch[1].type == Type.RAKE:
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
            if ll:
                ll.p = rt

            self.pushup(ll)
            self.pushup(rr)
            self.pushup(rt)

    def link(self, u, w, v):
        if u.id > v.id:
            u, v = v, u
        nnu = u.handle
        nnv = v.handle
        if not nnu and not nnv:
            return self.edge(u, w, v)

        ee = self.edge(u, w, v)
        ll = None

        if nnv:
            vv = self.expose(nnv)
            self.propagate(vv)
            if vv.vs[1] == v:
                self.set_toggle(vv)

            if vv.vs[0] == v:
                ll = self.compress(ee, vv)
            else:
                nv = vv
                self.propagate(nv)
                ch = nv.ch[0]
                self.propagate(ch)
                nv.ch[0] = ee
                ee.p = nv
                self.pushup(ee)

                bt = nv.q
                rk = self.rake(bt, ch) if bt else ch
                if bt:
                    bt.p = rk
                    ch.p = rk
                    self.pushup(bt)
                    self.pushup(ch)

                nv.q = rk
                if rk:
                    rk.p = nv
                self.pushup(rk)
                self.pushup(nv)
                ll = nv
        else:
            ll = ee

        if nnu:
            uu = self.expose(nnu)
            self.propagate(uu)
            if uu.vs[0] == u:
                self.set_toggle(uu)

            if uu.vs[1] == u:
                tp = self.compress(uu, ll)
                self.pushup(tp)
            else:
                nu = uu
                self.propagate(nu)
                ch = nu.ch[1]
                if ch:
                    self.toggle(ch)
                    self.propagate(ch)

                nu.ch[1] = ll
                ll.p = nu
                self.pushup(ll)

                al = nu.q
                rk = self.rake(al, ch) if al else ch
                if al:
                    al.p = rk
                    if ch:
                        ch.p = rk
                    self.pushup(al)
                    if ch:
                        self.pushup(ch)

                nu.q = rk
                if rk:
                    rk.p = nu
                self.pushup(rk)
                self.pushup(nu)
        return ee

    def cut(self, u, v):
        self.soft_expose(u, v)
        rt = u.handle
        self.propagate(rt)

        rr = rt.ch[1]
        rr.p = None
        self.set_toggle(rr)

        self.bring(rr)
        self.bring(rt)

    def path(self, u, v):
        self.soft_expose(u, v)
        rt = u.handle
        self.propagate(rt)
        if rt.ch[1]:
            self.propagate(rt.ch[1])
            if rt.ch[1].ch[0]:
                return rt.ch[1].ch[0]
        return None

    def get_path(self, u, v):
        p = self.path(u, v)
        return p.dat if p else Cluster()

    def find_1_median(self, v):
        self.expose(v.handle)
        rt = v.handle
        return self.find_median_in_cluster(rt, 0, 0)

    def get_1_median_value(self, v):
        w = self.find_1_median(v)
        rt = self.expose(w.handle)
        self.propagate(rt)
        if w == rt.vs[0] or w == rt.vs[1]:
            if rt.vs[0] != w:
                self.set_toggle(rt)
            return rt.dat.sum_dist_left
        else:
            sub = w.handle
            self.splay(sub)
            left = sub.ch[0]
            right = sub.ch[1]
            q = sub.q
            sum_left = left.dat.sum_dist_right if left else 0
            sum_right = right.dat.sum_dist_left if right else 0
            sum_side = q.dat.sum_dist_right if q else 0
            return sum_left + sum_right + sum_side

    def toggle_weight(self, v):
        v.weight = 1 - v.weight
        self.recursive_pushup(v.handle)
        t = v.handle.p
        while t:
            self.pushup(t)
            t = t.p

N, Q = map(int, input().split())
tt = TopTree()
vertices = [None] + [tt.create(i, weight=1) for i in range(1, N + 1)]
prev = 0
result = []
for _ in range(Q):
    k, *args = map(int, input().split())
    if k == 1:
        a, b, c = args

        a = (a - 1 + prev) % N + 1
        b = (b - 1 + prev) % N + 1
        # print("link", a, b, c)
        tt.link(vertices[a], Cluster(c), vertices[b])
    elif k == 2:
        a, b = args

        a = (a - 1 + prev) % N + 1
        b = (b - 1 + prev) % N + 1
        # print("cut", a, b)
        tt.cut(vertices[a], vertices[b])
    elif k == 3:
        a = args[0]
        a = (a - 1 + prev) % N + 1
        # print("query",a)
        tt.toggle_weight(vertices[a])
        S = tt.get_1_median_value(vertices[a])
        prev = (prev + S) % N
        result.append(S)
print("\n".join(map(str, result)))