import sys
import heapq

input = sys.stdin.readline
N, M, K = map(int, input().split())
start, end = map(int, input().split())

graph = [[] for _ in range(N + 1)]
INF = sys.maxsize
for _ in range(M):
    a, b, c = map(int, input().split())
    graph[a].append((b, c))
    graph[b].append((a, c))

max_edges = N - 1
dp = [[INF] * (N + 1) for _ in range(max_edges + 1)]
dp[0][start] = 0
pq = [(0, start, 0)]
while pq:
    cost, cur, used = heapq.heappop(pq)
    flag = False

    for i in range(used + 1):
        if dp[i][cur] < cost:
            flag = True
            break

    if used == max_edges or flag:
        continue
    for nxt, w in graph[cur]:
        if used + 1 <= max_edges and dp[used + 1][nxt] > cost + w:
            dp[used + 1][nxt] = cost + w
            heapq.heappush(pq, (dp[used + 1][nxt], nxt, used + 1))


def get_best(end,tax,edge):
    result = INF
    max_edges = N
    for i in range(edge,-1,-1):
        dp[i][end] = dp[i][end] + i * tax
        if result > dp[i][end]:
            max_edges = i
            result = dp[i][end]
    return result,max_edges

answer = []

cost,next_edge = get_best(end,0,max_edges)
answer.append(cost)

for _ in range(K):
    t = int(input())
    cost,next_edge = get_best(end, t, next_edge)
    answer.append(cost)

print('\n'.join(map(str, answer)))