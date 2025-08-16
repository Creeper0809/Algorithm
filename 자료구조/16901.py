import sys

class TrieNode:
    def __init__(self):
        self.children = [None, None]  # 0과 1 자식 노드

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, num):
        node = self.root
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if node.children[bit] is None:
                node.children[bit] = TrieNode()
            node = node.children[bit]

    def min_xor(self, num):
        node = self.root
        res = 0
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            res <<= 1
            if node.children[bit] is not None:
                node = node.children[bit]
            else:
                res += 1
                node = node.children[1 - bit]
        return res

def dfs(arr):
    n = len(arr)
    if n <= 1:
        return 0
    if n == 2:
        return arr[0] ^ arr[1]
    if n == 3:
        edges = [arr[0] ^ arr[1], arr[0] ^ arr[2], arr[1] ^ arr[2]]
        edges.sort()
        return edges[0] + edges[1]

    xor_all = 0
    for x in arr:
        xor_all |= arr[0] ^ x
    if xor_all == 0:
        return 0

    bit = 31
    while (xor_all & (1 << bit)) == 0:
        bit -= 1

    left = []
    right = []
    for x in arr:
        if (x & (1 << bit)) == 0:
            left.append(x)
        else:
            right.append(x)

    cost_left = dfs(left)
    cost_right = dfs(right)

    if not left or not right:
        return cost_left + cost_right

    trie = Trie()
    if len(left) <= len(right):
        small, large = left, right
    else:
        small, large = right, left
    for x in small:
        trie.insert(x)
    min_cost = float('inf')
    for x in large:
        min_cost = min(min_cost, trie.min_xor(x))

    return cost_left + cost_right + min_cost

input = sys.stdin.readline
N = int(input().strip())
A = list(map(int, input().strip().split()))

total_cost = dfs(A)
print(total_cost)