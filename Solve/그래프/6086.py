import math
from collections import deque

size = 60

def maxFlow(capacity, source, sink):
    flow = [[0] * size for _ in range(size)]
    total_flow = 0
    while True:
        queue = deque([source])
        parent = [-1] * size
        parent[source] = source
        while len(queue) != 0:
            next = queue.popleft()
            for i in range(size):
                if parent[i] == -1 and capacity[next][i] - flow[next][i] > 0:
                    queue.append(i)
                    parent[i] = next
        if parent[sink] == -1:
            return total_flow
        p = sink
        amount = 1e10
        while p != source:
            amount = min(amount, capacity[parent[p]][p] - flow[parent[p]][p])
            p = parent[p]
        total_flow += amount
        p = sink
        while p != source:
            flow[parent[p]][p] += amount
            flow[p][parent[p]] -= amount
            p = parent[p]


def solution():
    n = int(input())
    capacity = [[0] * size for _ in range(size)]
    for _ in range(n):
        _from, _to, weight = input().split()
        _from = ord(_from)-65
        _to = ord(_to)-65
        weight = int(weight)
        capacity[_from][_to] += weight
        capacity[_to][_from] += weight
    print(maxFlow(capacity, ord('A')-65, ord('Z')-65))


solution()