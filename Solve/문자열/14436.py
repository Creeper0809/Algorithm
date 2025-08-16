import sys

# 재귀 깊이 제한을 늘려줍니다. (LCT, SA의 재귀적 호출 가능성)
sys.setrecursionlimit(400000 * 4)

# 빠른 입력을 위한 설정
input = sys.stdin.readline


class FenwickTree:
    """펜윅 트리(Fenwick Tree) 또는 이진 인덱스 트리(Binary Indexed Tree)"""

    def __init__(self, size):
        self.tree = [0] * (size + 1)

    def add(self, i, delta):
        """i번째 원소에 delta를 더합니다."""
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & -i

    def query(self, i):
        """1번째부터 i번째 원소까지의 누적 합을 구합니다."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

    def query_range(self, i, j):
        """i부터 j까지의 구간 합을 구합니다."""
        if i > j: return 0
        res = self.query(j)
        if i > 1:
            res -= self.query(i - 1)
        return res


class LinkCutNode:
    """LCT의 각 노드. Splay Tree 노드이기도 합니다."""

    def __init__(self):
        # LCT 구조를 위한 포인터
        self.p = self.l = self.r = None
        # Lazy Propagation을 위한 값들
        self.rev = False
        self.lazy_pos = 0

        # SA 상태와 관련된 정보
        self.len = 0
        self.link_len = 0
        self.max_pos = -1

    def get_contribution(self):
        """이 상태가 단독으로 기여하는 부분 문자열의 개수"""
        return self.len - self.link_len

    def get_key(self):
        """펜윅 트리에서 사용할 인덱스 키"""
        if self.max_pos == -1:
            return -1
        return self.max_pos - self.len

    def is_root(self):
        """Splay Tree의 루트인지 확인"""
        return not self.p or (self.p.l is not self and self.p.r is not self)

    def push(self):
        """Lazy 값을 자식에게 전파"""
        if self.rev:
            self.l, self.r = self.r, self.l
            if self.l: self.l.rev ^= True
            if self.r: self.r.rev ^= True
            self.rev = False

        if self.lazy_pos:
            if self.l: self.l.apply_lazy(self.lazy_pos)
            if self.r: self.r.apply_lazy(self.lazy_pos)
            self.lazy_pos = 0

    def apply_lazy(self, pos_val):
        """Lazy 업데이트를 현재 노드에 적용"""
        # 펜윅 트리에서 기존 값 제거
        old_key = self.get_key()
        if old_key != -1:
            ft.add(offset + old_key, -self.get_contribution())

        # max_pos 갱신 및 펜윅 트리에 새 값 추가
        self.max_pos = pos_val
        new_key = self.get_key()
        ft.add(offset + new_key, self.get_contribution())

        # lazy_pos 갱신
        self.lazy_pos = pos_val

    def rotate(self):
        """Splay Tree의 rotate 연산"""
        p, g = self.p, self.p.p
        if not p.is_root():
            g.attach(self, p is g.r)
        else:
            self.p = g

        if self is p.l:
            p.attach(self.r, False); self.attach(p, True)
        else:
            p.attach(self.l, True); self.attach(p, False)

    def attach(self, node, is_right):
        """자식 노드를 연결하고, 부모 포인터를 설정"""
        if is_right:
            self.r = node
        else:
            self.l = node
        if node: node.p = self

    def splay(self):
        """노드를 Splay Tree의 루트로 만듦"""
        path = []
        node = self
        while True:
            path.append(node)
            if node.is_root(): break
            node = node.p
        for node in reversed(path): node.push()

        while not self.is_root():
            p, g = self.p, self.p.p
            if not p.is_root():
                if (self is p.l) == (p is g.l):
                    p.rotate()
                else:
                    self.rotate()
            self.rotate()

    def access(self):
        """노드에서 실제 트리의 루트까지를 주 경로(preferred path)로 만듦"""
        last = None
        x = self
        while x:
            x.splay()
            x.r = last
            last = x
            x = x.p
        self.splay()

    def make_root(self):
        self.access()
        self.rev = not self.rev

    def link(self, parent):
        self.make_root()
        self.p = parent

    def cut(self):
        self.access()
        if self.l:
            self.l.p = None
            self.l = None


class SuffixAutomaton:
    """접미사 오토마타와 LCT를 함께 관리하는 클래스"""

    def __init__(self, n_max):
        # LCT 노드와 SA 상태를 1:1로 매칭
        self.nodes = [LinkCutNode() for _ in range(2 * n_max + 2)]
        self.sz = 1
        self.last = 0
        self.nodes[0].len = 0
        self.nodes[0].link_len = 0  # 루트의 링크는 없으므로 0
        self.adj = [{} for _ in range(2 * n_max + 2)]

    def extend(self, c, current_pos):
        """문자 c를 추가하여 SA를 확장"""
        cur = self.sz
        self.sz += 1
        self.nodes[cur].len = self.nodes[self.last].len + 1

        # LCT: 새로운 노드의 max_pos를 설정하고 펜윅 트리에 추가
        self.nodes[cur].max_pos = current_pos
        key = self.nodes[cur].get_key()
        # 링크가 정해지기 전이므로 기여도는 임시로 len만 사용
        ft.add(offset + key, self.nodes[cur].len)

        p = self.last
        while p is not None and c not in self.adj[p]:
            self.adj[p][c] = cur
            # LCT의 부모 포인터는 SA의 link와 반대 방향임
            # 실제 트리의 부모를 찾기 위해 access 후 left child를 따라가야 하지만,
            # SA의 link는 LCT의 path-parent 포인터로 관리되므로 self.nodes[p].p로 접근
            p_node = self.nodes[p]
            parent_node = p_node.p
            if parent_node:
                p = self.nodes.index(parent_node) if parent_node in self.nodes else None
            else:  # 루트에 도달
                p = None

        if p is None:
            self.nodes[cur].link(self.nodes[0])
        else:
            q_idx = self.adj[p][c]
            q_node = self.nodes[q_idx]
            p_node = self.nodes[p]

            if q_node.len == p_node.len + 1:
                self.nodes[cur].link(q_node)
            else:
                clone_idx = self.sz
                self.sz += 1
                clone_node = self.nodes[clone_idx]

                clone_node.len = p_node.len + 1
                self.adj[clone_idx] = self.adj[q_idx].copy()

                q_node.cut()
                q_node.link(clone_node)

                if clone_node.p:  # 이전 q의 부모가 있었다면
                    clone_node.link(clone_node.p)  # 이 부분은 LCT구현에 따라 달라질 수 있음

                # 펜윅 트리 업데이트 (clone 생성)
                clone_node.max_pos = q_node.max_pos
                clone_key = clone_node.get_key()
                clone_link_len = clone_node.p.len if clone_node.p else 0
                ft.add(offset + clone_key, clone_node.len - clone_link_len)

                # 펜윅 트리 업데이트 (q의 링크 변경)
                q_key = q_node.get_key()
                ft.add(offset + q_key, -(q_node.len - q_node.link_len))
                ft.add(offset + q_key, q_node.len - clone_node.len)

                clone_node.link_len = clone_link_len
                q_node.link_len = clone_node.len

                while p is not None and self.adj[p].get(c) == q_idx:
                    self.adj[p][c] = clone_idx
                    p_node = self.nodes[p]
                    parent_node = p_node.p
                    if parent_node:
                        p = self.nodes.index(parent_node) if parent_node in self.nodes else None
                    else:
                        p = None

                self.nodes[cur].link(clone_node)

        # 펜윅 트리 업데이트 (cur의 링크 확정)
        cur_link_node = self.nodes[cur].p
        self.nodes[cur].link_len = cur_link_node.len if cur_link_node else 0
        ft.add(offset + key, -self.nodes[cur].link_len)  # 이전에 더했던 len에서 link_len을 뺌

        self.last = cur

        # LCT 경로 업데이트
        path_update_node = self.nodes[cur]
        path_update_node.access()
        path_update_node.apply_lazy(current_pos)


# --- 메인 로직 ---
MOD = 1_000_000_007
Q = int(input())
MAX_LEN = Q
ft = FenwickTree(2 * MAX_LEN + 5)
offset = MAX_LEN + 2

sa = SuffixAutomaton(MAX_LEN)
l, r = 1, 0
total_ans = 0

for _ in range(Q):
    query = input().split()
    op = query[0]

    if op == '+':
        r += 1
        char_code = ord(query[1]) - ord('a')
        sa.extend(char_code, r)
    else:  # op == '-'
        l += 1

    # 펜윅 트리로 현재 윈도우 [l, r]에 대한 답을 쿼리
    # key (max_pos - len) >= l - 1 인 모든 상태의 기여도를 합산
    current_ans = ft.query_range(offset + l - 1, 2 * MAX_LEN + 5)
    total_ans = (total_ans + current_ans) % MOD

print(total_ans)
