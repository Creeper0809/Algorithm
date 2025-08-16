import sys
import math


class LinkCutTree:
    __slots__ = ['MAX', 'vertices', 'free_node_ids', 'root']
    def __init__(self, n, max_nodes=150005):
        self.MAX = max_nodes
        self.vertices = [self.Node() for _ in range(max_nodes)]
        self.free_node_ids = list(range(n + 1, max_nodes))
        self.root = None

    class Data:
        __slots__ = ['total_sum', 'min_val', 'max_val', 'size']
        def __init__(self, value=0):
            self.total_sum = value
            self.min_val = value if value else math.inf
            self.max_val = value if value else -math.inf
            self.size = 1 if value else 0

        def __add__(self, other):
            data = LinkCutTree.Data()
            data.total_sum = self.total_sum + other.total_sum
            data.min_val = min(self.min_val, other.min_val)
            data.max_val = max(self.max_val, other.max_val)
            data.size = self.size + other.size
            return data

        def _apply_data(self, data):
            temp = self + data
            self.total_sum = temp.total_sum
            self.min_val = temp.min_val
            self.max_val = temp.max_val
            self.size = temp.size

        def _apply_lazy(self, data):
            if self.size:
                self.total_sum = self.total_sum * data.is_set + self.size * data.val
                self.min_val = self.min_val * data.is_set + data.val
                self.max_val = self.max_val * data.is_set + data.val

        def apply_data(self, other):
            if isinstance(other, LinkCutTree.Data):
                self._apply_data(other)
            else:
                self._apply_lazy(other)
            return self

    class Lazy:
        __slots__ = ['is_set', 'val']
        def __init__(self, is_set=False, val=0):
            self.is_set = 0 if is_set else 1
            self.val = val

        def is_lazy(self):
            return self.is_set != 1 or self.val != 0

        def __iadd__(self, other):
            self.is_set = self.is_set * other.is_set
            self.val = self.val * other.is_set + other.val
            return self

    class Node:
        __slots__ = ['p', 'ch', 'val', 'path', 'sub', 'all', 'path_lazy', 'sub_lazy', 'flipped', 'is_fake']
        def __init__(self, value=None):
            self.p = 0
            self.ch = [0] * 4
            self.val = 0
            self.path = LinkCutTree.Data()
            self.sub = LinkCutTree.Data()
            self.all = LinkCutTree.Data()
            self.path_lazy = LinkCutTree.Lazy()
            self.sub_lazy = LinkCutTree.Lazy()
            self.flipped = False
            self.is_fake = True
            if value is not None:
                self.val = value
                self.path = LinkCutTree.Data(value)
                self.all = LinkCutTree.Data(value)
                self.is_fake = False

    def apply_lazy_to_value(self, value, lazy):
        return value * lazy.is_set + lazy.val

    def propagate_flip(self, u):
        if not u:
            return
        self.vertices[u].ch[0], self.vertices[u].ch[1] = \
            self.vertices[u].ch[1], self.vertices[u].ch[0]
        self.vertices[u].flipped = not self.vertices[u].flipped

    def propagate_path(self, u, lazy):
        if not u or self.vertices[u].is_fake:
            return
        self.vertices[u].val = self.apply_lazy_to_value(self.vertices[u].val, lazy)
        self.vertices[u].path.apply_data(lazy)
        self.vertices[u].all = self.vertices[u].path + self.vertices[u].sub
        self.vertices[u].path_lazy += lazy

    def propagate_sub(self, u, apply_to_path, lazy):
        if not u:
            return
        self.vertices[u].sub.apply_data(lazy)
        self.vertices[u].sub_lazy += lazy
        if not self.vertices[u].is_fake and apply_to_path:
            self.propagate_path(u, lazy)
        else:
            self.vertices[u].all = self.vertices[u].path + self.vertices[u].sub

    def propagate(self, u):
        if not u:
            return
        if self.vertices[u].flipped:
            self.propagate_flip(self.vertices[u].ch[0])
            self.propagate_flip(self.vertices[u].ch[1])
            self.vertices[u].flipped = False
        if self.vertices[u].path_lazy.is_lazy():
            self.propagate_path(self.vertices[u].ch[0], self.vertices[u].path_lazy)
            self.propagate_path(self.vertices[u].ch[1], self.vertices[u].path_lazy)
            self.vertices[u].path_lazy = self.Lazy()
        if self.vertices[u].sub_lazy.is_lazy():
            self.propagate_sub(self.vertices[u].ch[0], False, self.vertices[u].sub_lazy)
            self.propagate_sub(self.vertices[u].ch[1], False, self.vertices[u].sub_lazy)
            self.propagate_sub(self.vertices[u].ch[2], True, self.vertices[u].sub_lazy)
            self.propagate_sub(self.vertices[u].ch[3], True, self.vertices[u].sub_lazy)
            self.vertices[u].sub_lazy = self.Lazy()

    def update(self, u):
        if not self.vertices[u].is_fake:
            l = self.vertices[self.vertices[u].ch[0]].path
            value = self.Data(self.vertices[u].val)
            r = self.vertices[self.vertices[u].ch[1]].path
            self.vertices[u].path = l + value + r
        sub_l = self.vertices[self.vertices[u].ch[0]].sub
        sub_r = self.vertices[self.vertices[u].ch[1]].sub
        self.vertices[u].sub = (sub_l + sub_r
                                + self.vertices[self.vertices[u].ch[2]].all
                                + self.vertices[self.vertices[u].ch[3]].all)
        self.vertices[u].all = self.vertices[u].path + self.vertices[u].sub

    def attach_child(self, p, dir, ch):
        self.vertices[p].ch[dir] = ch
        if ch:
            self.vertices[ch].p = p
        self.update(p)

    def get_dir(self, ch, dir):
        p = self.vertices[ch].p
        if self.vertices[p].ch[dir] == ch:
            return dir
        elif self.vertices[p].ch[dir + 1] == ch:
            return dir + 1
        return -1

    def rotate(self, ch, dir):
        p = self.vertices[ch].p
        grand_p = self.vertices[p].p
        ch_dir = self.get_dir(ch, dir)
        p_dir = self.get_dir(p, dir)
        if p_dir == -1 and dir == 0:
            p_dir = self.get_dir(p, 2)
        self.attach_child(p, ch_dir, self.vertices[ch].ch[ch_dir ^ 1])
        self.attach_child(ch, ch_dir ^ 1, p)
        if p_dir != -1:
            self.attach_child(grand_p, p_dir, ch)
        else:
            self.vertices[ch].p = grand_p

    def splay(self, u, dir):
        self.propagate(u)
        while (self.get_dir(u, dir) != -1 and
               (dir == 0 or self.vertices[self.vertices[u].p].is_fake)):
            p = self.vertices[u].p
            grand_p = self.vertices[p].p
            self.propagate(grand_p)
            self.propagate(p)
            self.propagate(u)
            child_dir = self.get_dir(u, dir)
            parent_dir = self.get_dir(p, dir)
            if (parent_dir != -1 and
                    (dir == 0 or self.vertices[grand_p].is_fake)):
                if child_dir == parent_dir:
                    self.rotate(p, dir)
                else:
                    self.rotate(u, dir)
            self.rotate(u, dir)

    def add_subtree(self, p, ch):
        if not ch:
            return
        for i in range(2, 4):
            if not self.vertices[p].ch[i]:
                self.attach_child(p, i, ch)
                return
        new_node = self.free_node_ids.pop()
        self.vertices[new_node] = self.Node()  # fake node 초기화
        self.attach_child(new_node, 2, self.vertices[p].ch[2])
        self.attach_child(new_node, 3, ch)
        self.attach_child(p, 2, new_node)

    def push_down(self, u):
        if self.vertices[u].is_fake:
            self.push_down(self.vertices[u].p)
        self.propagate(u)

    def remove_subtree(self, ch):
        p = self.vertices[ch].p
        self.push_down(p)
        if self.vertices[p].is_fake:
            grandparent_id = self.vertices[p].p
            self.attach_child(grandparent_id,
                              self.get_dir(p, 2),
                              self.vertices[p].ch[self.get_dir(ch, 2) ^ 1])
            if self.vertices[grandparent_id].is_fake:
                self.splay(grandparent_id, 2)
            self.free_node_ids.append(p)
        else:
            self.attach_child(p, self.get_dir(ch, 2), 0)
        self.vertices[ch].p = 0

    def get_parent(self, u):
        p = self.vertices[u].p
        if not self.vertices[p].is_fake:
            return p
        self.splay(p, 2)
        return self.vertices[p].p

    def access(self, node_id):
        prev = node_id
        self.splay(node_id, 0)
        self.add_subtree(node_id, self.vertices[node_id].ch[1])
        self.attach_child(node_id, 1, 0)
        while self.vertices[node_id].p:
            prev = self.get_parent(node_id)
            self.splay(prev, 0)
            self.remove_subtree(node_id)
            self.add_subtree(prev, self.vertices[prev].ch[1])
            self.attach_child(prev, 1, node_id)
            self.splay(node_id, 0)
        return prev

    def change_root(self,node_id):
        self.root = node_id

    def evert(self, node_id):
        self.access(node_id)
        self.propagate_flip(node_id)

    def link(self, node_u, node_v):
        self.evert(node_u)
        self.access(node_v)
        self.add_subtree(node_v, node_u)

    def cut(self, node_u, node_v):
        self.evert(node_u)
        self.access(node_v)
        self.vertices[node_v].ch[0] = self.vertices[node_u].p = 0
        self.update(node_v)

    def set_vertex_weight(self, node_id, value):
        self.vertices[node_id] = self.Node(value)

    def subtree_query(self, target_node):
        self.evert(self.root)
        self.access(target_node)
        result = self.Data(self.vertices[target_node].val)
        for i in range(2, 4):
            result = result + self.vertices[self.vertices[target_node].ch[i]].all
        return result

    def _subtree_update(self, u, value, is_set):
        self.evert(self.root)
        self.access(u)
        lazy = self.Lazy(is_set, value)
        self.vertices[u].val = self.apply_lazy_to_value(
            self.vertices[u].val, lazy)
        for i in range(2, 4):
            self.propagate_sub(self.vertices[u].ch[i], True, lazy)

    def subtree_add(self, u, value):
        self._subtree_update(u, value, False)

    def subtree_set(self, u, value):
        self._subtree_update(u, value, True)

    def path_query(self, start_node, end_node):
        self.evert(start_node)
        self.access(end_node)
        data = self.vertices[end_node].path
        return data

    def _path_update(self, u, v, value, is_set):
        self.evert(u)
        self.access(v)
        lazy = self.Lazy(is_set=is_set, val=value)
        self.propagate_path(v, lazy)

    def add_path(self, u, v, value):
        self._path_update(u, v, value, False)

    def set_path(self, u, v, value):
        self._path_update(u, v, value, True)

    def change_parent(self, node_x, node_y):
        self.evert(self.root)
        self.access(node_y)
        if self.access(node_x) != node_x:
            self.vertices[node_x].ch[0] = self.vertices[self.vertices[node_x].ch[0]].p = 0
            self.update(node_x)
            self.access(node_y)
            self.add_subtree(node_y, node_x)


def main():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    lct = LinkCutTree(N)

    edge_list = []
    for _ in range(N - 1):
        u, v = map(int, input().split())
        edge_list.append((u, v))

    for i in range(1, N + 1):
        weight = int(input())
        lct.set_vertex_weight(i, weight)

    for u, v in edge_list:
        lct.link(u, v)

    lct.change_root(int(input()))
    answer = []

    for _ in range(M):
        k, *arg = map(int, input().split())
        if k == 1:
            r = arg[0]
            lct.change_root(r)
        elif k in [3, 4, 11]:
            x = arg[0]
            result = lct.subtree_query(x)
            if k == 3:
                answer.append(result.min_val)
            elif k == 4:
                answer.append(result.max_val)
            elif k == 11:
                answer.append(result.total_sum)
        elif k == 0:
            x,y = arg
            lct.subtree_set(x, y)
        elif k == 5:
            x, y = arg
            lct.subtree_add(x, y)
        elif k in [7, 8, 10]:
            x,y = arg
            result = lct.path_query(x, y)
            if k == 7:
                answer.append(result.min_val)
            elif k == 8:
                answer.append(result.max_val)
            elif k == 10:
                answer.append(result.total_sum)
        elif k == 2:
            x, y, z = arg
            lct.set_path(x, y, z)
        elif k == 6:
            x, y, z = arg
            lct.add_path(x, y, z)
        else:
            x, y = arg
            lct.change_parent(x, y)

    print("\n".join(map(str, answer)))


if __name__ == "__main__":
    main()