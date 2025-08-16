import sys
input = sys.stdin.readline
class Node:
    def __init__(self):
        self.child = {}
        self.endOfWord = False
root_node = Node()

def insert(words):
    for word in words:
        node = root_node
        for i in range(len(word)):
            char = word[i]
            if char not in node.child:
                node.child[char] = Node()
            node = node.child[char]
        node.endOfWord = True

def search(words):
    result = 0
    for word in words:
        node = root_node.child[word[0]]
        temp = 1
        for i in range(1,len(word)):
            char = word[i]
            if len(node.child) != 1 or node.endOfWord:
                temp += 1
            node = node.child[char]
        result += temp
    return result

while True:
    line = input()
    if not line:
        break
    N = line.strip()
    if N == "":
        continue
    temp = list()
    N = int(N)
    root_node = Node()
    for _ in range(N):
        temp.append(input().strip())
    insert(temp)
    print('%.2f' % (search(temp)/N))
