import sys; input = sys.stdin.readline
sys.setrecursionlimit(10**6)

BITS = 30
ALL = (1 << BITS) - 1
N = int(input())
arr = list(map(int,input().split()))

class Node:
    def __init__(self):
        self.max_val = sys.maxsize
        self.one_mask = 0
        self.zero_mask = ALL
        self.lazy_and = 0
        self.lazy_or = 0

seg_tree = [Node() for _ in range(N * 4)]

def build_tree(node, start, end):
    if start == end:
        seg_tree[node].max_val = arr[start]
        seg_tree[node].one_mask = arr[start]
        seg_tree[node].zero_mask = (~arr[start]) & ALL
        return

    mid = (start + end) // 2
    build_tree(node * 2, start, mid)
    build_tree(node * 2 + 1, mid + 1, end)

    left_node = seg_tree[node * 2]
    right_node = seg_tree[node * 2 + 1]

    seg_tree[node].max_val = min(left_node.max_val, right_node.max_val)
    seg_tree[node].one_mask = left_node.one_mask & right_node.one_mask
    seg_tree[node].zero_mask = left_node.zero_mask & right_node.zero_mask


def apply(node, start, end):
    now_node = seg_tree[node]

    now_node.max_val |= now_node.lazy_or
    now_node.one_mask |= now_node.lazy_or
    now_node.zero_mask &= (~now_node.lazy_or) & ALL

    now_node.max_val &= (~now_node.lazy_and) & ALL
    now_node.one_mask &= (~now_node.lazy_and) & ALL
    now_node.zero_mask |= now_node.lazy_and

    if start != end:
        left_node = seg_tree[node * 2]
        right_node = seg_tree[node * 2 + 1]

        left_node.lazy_or &= (~now_node.lazy_and) & ALL
        left_node.lazy_and &= (~now_node.lazy_or) & ALL
        left_node.lazy_or |= now_node.lazy_or
        left_node.lazy_and |= now_node.lazy_and

        right_node.lazy_or &= (~now_node.lazy_and) & ALL
        right_node.lazy_and &= (~now_node.lazy_or) & ALL
        right_node.lazy_or |= now_node.lazy_or
        right_node.lazy_and |= now_node.lazy_and

    now_node.lazy_or = 0
    now_node.lazy_and = 0

def query(node, start, end,left,right):
    apply(node, start, end)
    if right < start or left > end:
        return sys.maxsize
    if left <= start and end <= right:
        return seg_tree[node].max_val
    mid = (start+end)//2
    return min(query(node * 2,start,mid,left,right), query(node*2 + 1,mid+1,end,left,right))

def update_or(node, start, end,left,right,value):
    apply(node, start, end)
    if right < start or left > end:
        return

    now_node = seg_tree[node]
    value &= (~now_node.one_mask) & ALL

    if left <= start and end <= right and (value & now_node.zero_mask):
        update_bits = value & now_node.zero_mask
        now_node.lazy_or = update_bits
        value &= (~update_bits) & ALL
        apply(node, start, end)

    if value == 0:
        return

    mid = (start + end) // 2

    update_or(2 * node, start, mid, left, right, value)
    update_or(2 * node + 1, mid + 1, end, left, right, value)

    left_node = seg_tree[2 * node]
    right_node = seg_tree[2 * node + 1]

    seg_tree[node].one_mask = left_node.one_mask & right_node.one_mask
    seg_tree[node].zero_mask = left_node.zero_mask & right_node.zero_mask
    seg_tree[node].max_val = min(left_node.max_val, right_node.max_val)

def update_and(node, start, end,left,right,value):
    apply(node, start, end)
    if right < start or left > end:
        return

    now_node = seg_tree[node]
    value &= (~now_node.zero_mask) & ALL

    if left <= start and end <= right and (value & now_node.one_mask):
        update_bits = value & now_node.one_mask
        now_node.lazy_and = update_bits
        value &= (~update_bits) & ALL
        apply(node, start, end)

    if value == 0:
        return

    mid = (start + end) // 2

    update_and(2*node, start, mid, left, right, value)
    update_and(2*node + 1, mid + 1, end, left, right, value)

    left_node = seg_tree[2*node]
    right_node = seg_tree[2*node+1]

    seg_tree[node].one_mask = left_node.one_mask & right_node.one_mask
    seg_tree[node].zero_mask = left_node.zero_mask & right_node.zero_mask
    seg_tree[node].max_val = min(left_node.max_val, right_node.max_val)

build_tree(1,0,N-1)

M = int(input())
query_result = []
for _ in range(M):
    query_list = input().rstrip().split()
    if query_list[0] == "&":
        update_and(1,0,N-1,int(query_list[1]) - 1,int(query_list[2]) - 1,(~int(query_list[3])) & ALL)
    elif query_list[0] == "|":
        update_or(1,0,N-1,int(query_list[1]) - 1,int(query_list[2]) - 1,int(query_list[3]))
    else:
        query_result.append(query(1,0,N-1,int(query_list[1]) -1 ,int(query_list[2]) - 1))

print("\n".join(map(str,query_result)))