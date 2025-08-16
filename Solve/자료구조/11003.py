from collections import deque

N,L = map(int,input().split())
arr = list(map(int,input().split()))

queue = deque()

for index,element in enumerate(arr):
    while queue and queue[0][0] <= index - L:
        queue.popleft()
    while queue and element < queue[-1][1]:
        queue.pop()
    queue.append((index,element))
    print(queue[0][1], end= " ")
