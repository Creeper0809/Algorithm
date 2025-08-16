from collections import deque
import sys

class Node:
    def __init__(self):
        self.children = [None] * 26
        self.fail = None
        self.output = []

class AhoCorasick:
    def __init__(self):
        self.root = Node()
        self.root.fail = self.root
        self.pattern_lengths = {}

    def add_pattern(self, pattern, id):
        node = self.root
        for char in pattern:
            idx = ord(char) - ord('a')
            if self.root.children[idx] is None:  # 클래스 초기화에서 None으로 설정
                pass
            if node.children[idx] is None:
                node.children[idx] = Node()
            node = node.children[idx]
        node.output.append(id)
        self.pattern_lengths[id] = len(pattern)

    def build_fail(self):
        queue = deque()
        for i in range(26):
            if self.root.children[i]:
                self.root.children[i].fail = self.root
                queue.append(self.root.children[i])
        while queue:
            current = queue.popleft()
            for i in range(26):
                if current.children[i]:
                    child = current.children[i]
                    fail = current.fail
                    while fail != self.root and fail.children[i] is None:
                        fail = fail.fail
                    if fail.children[i]:
                        fail = fail.children[i]
                    child.fail = fail if (fail != self.root or self.root.children[i]) else self.root
                    child.output = child.output + child.fail.output
                    queue.append(child)

    def build_transitions(self):
        queue = deque()
        for i in range(26):
            if self.root.children[i]:
                queue.append(self.root.children[i])
            else:
                self.root.children[i] = self.root
        while queue:
            current = queue.popleft()
            for i in range(26):
                if current.children[i]:
                    queue.append(current.children[i])
                else:
                    current.children[i] = current.fail.children[i]

input = sys.stdin.readline
S = input().strip()
N = int(input().strip())
patterns = [input().strip() for _ in range(N)]
ac = AhoCorasick()
for i, p in enumerate(patterns):
    ac.add_pattern(p, i)
ac.build_fail()
ac.build_transitions()
result = []
state_history = [ac.root]
for char in S:
    current = state_history[-1]
    idx = ord(char) - ord('a')
    node = current.children[idx]
    result.append(char)
    state_history.append(node)
    if node.output:
        idx = node.output[0]
        pat_len = ac.pattern_lengths[idx]
        for _ in range(pat_len):
            result.pop()
            state_history.pop()
print(''.join(result))