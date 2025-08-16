from collections import deque

dir = [[1, 0], [-1, 0], [0, -1], [0, 1]]
R, C = map(int, input().split())
graph = [list(input()) for _ in range(R)]
def bfs(x,y):
    queue = deque()
    visited = [[[-1] * 2 for _ in range(C)] for _ in range(R)]