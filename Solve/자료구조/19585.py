N,M = map(int,input().split())
team_name = set()
class Node:
    def __init__(self):
        self.child = {}
        self.end_of_word = False

root_node = Node()

def insert(word):
    node = root_node
    for i in range(len(word)):
        char = word[i]
        if char not in node.child:
            node.child[char] = Node()
        node = node.child[char]
    node.end_of_word = True


def search(word):
    node = root_node
    for i,char in enumerate(word):
        if node.end_of_word and word[i:] in team_name:
            return True
        if char not in node.child:
            return False
        node = node.child[char]

for _ in range(N):
    word = input()
    insert(word)

for _ in range(M):
    word = input()
    team_name.add(word)

Q = int(input())

for i in range(Q):
    word = input()
    if search(word):
        print("Yes")
    else:
        print("No")