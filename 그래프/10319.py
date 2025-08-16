import sys
from collections import deque

N = int(input())
graph = list()
INF = sys.maxsize


class Edge:

    def __init__(self, to, capacity):
        self.capacity = capacity
        self.to = to
        self.flow = 0
        self.inverse_edge = None

    def getRemain(self):
        return self.capacity - self.flow

    def push(self, value):
        self.flow += value
        self.inverse_edge.flow -= value


def buildEdge(a, b, capacity):
    to, come = Edge(b, capacity), Edge(a, 0)
    come.inverse_edge = to
    to.inverse_edge = come
    graph[a].append(to)
    graph[b].append(come)


def BFS(source, visited, path):
    queue = deque()
    queue.append(source)
    while queue and visited[0] == -1:
        now = queue.popleft()
        for connectedEdge in graph[now]:
            there = connectedEdge.to
            if connectedEdge.getRemain() > 0 and visited[there] == -1:
                queue.append(there)
                visited[there] = now
                path[there] = connectedEdge
                if there == 0:
                    return True
    return False


def getFlow(source):
    total = 0
    while True:
        visited = [-1 for _ in range(len(graph))]
        path = [None for _ in range(len(graph))]
        if not BFS(source, visited, path):
            break
        minFlow = INF
        current = 0
        while current != source:
            minFlow = min(minFlow, path[current].getRemain())
            current = visited[current]

        current = 0
        while current != source:
            path[current].push(minFlow)
            current = visited[current]

        total += minFlow
        if total > 100:
            return 100
    return total


def solve():
    n = int(input())
    global graph
    graph = [list() for _ in range((n + 1) * 101)]
    maxCap, g, s = map(int, input().split())

    # 병원을 하나의 가상 정점 sink(0)으로 모음
    m = int(input())
    for _ in range(m):
        x = int(input())
        for time in range(s + 1):
            buildEdge(x * 101 + time, 0, INF)

    # 정점을 시간으로 분할
    r = int(input())
    for _ in range(r):
        a, b, p, t = map(int, input().split())
        for time in range(s - t + 1):
            buildEdge(a * 101 + time, b * 101 + time + t, p)

    # 가만히 있을 때를 고려
    for i in range(1, n + 1):
        for time in range(s):
            buildEdge(i * 101 + time, i * 101 + time + 1, INF)

    print(min(g, getFlow(maxCap * 101)))


while N != 0:
    solve()
    N -= 1