from collections import deque

queue = deque()
N = int(input())

for _ in range(N):
    command, *args = input().split()
    if command == 'push':
        queue.append(int(args[0]))
    if command == 'pop':
        if queue:
            print(queue.pop())
        else:
            print("-1")
    if command == 'size':
        print(len(queue))
    if command == 'front':
        print(queue[0] if queue else -1)
    if command == 'top':
        print(queue[-1] if queue else -1)
    if command == "empty":
        print(0 if queue else 1)