from collections import deque
import sys

input = sys.stdin.readline
INF = 10**18

class Edge:
    def __init__(self, destination, capacity, cost):
        self.destination = destination
        self.capacity = capacity
        self.cost = cost
        self.reverse_edge = None

def add_edge(adj_list, from_node, to_node, capacity, cost):
    forward = Edge(to_node, capacity, cost)
    backward = Edge(from_node, 0, -cost)

    forward.reverse_edge  = backward
    backward.reverse_edge = forward

    adj_list[from_node].append(forward)
    adj_list[to_node].append(backward)

def min_cost_max_flow(adj_list, start_node, end_node):
    num_nodes = len(adj_list)
    total_flow = 0
    total_cost = 0

    for _ in range(2):
        min_cost_to = [INF] * num_nodes
        in_queue = [False] * num_nodes
        prev_edge = [None] * num_nodes

        min_cost_to[start_node] = 0
        queue = deque([start_node])
        in_queue[start_node] = True

        while queue:
            curr_node = queue.popleft()
            in_queue[curr_node] = False

            for edge in adj_list[curr_node]:
                next_node = edge.destination
                if edge.capacity > 0 and min_cost_to[next_node] > min_cost_to[curr_node] + edge.cost:
                    min_cost_to[next_node] = min_cost_to[curr_node] + edge.cost
                    prev_edge[next_node]   = edge
                    if not in_queue[next_node]:
                        queue.append(next_node)
                        in_queue[next_node] = True

        if min_cost_to[end_node] == INF:
            break

        bottleneck = INF
        node = end_node
        while node != start_node:
            edge = prev_edge[node]
            bottleneck = min(bottleneck, edge.capacity)
            node = edge.reverse_edge.destination

        node = end_node
        while node != start_node:
            edge = prev_edge[node]
            rev_edge = edge.reverse_edge

            edge.capacity -= bottleneck
            rev_edge.capacity += bottleneck
            total_cost += edge.cost * bottleneck

            node = rev_edge.destination

        total_flow += bottleneck

    return total_flow, total_cost


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    N, M = map(int, line.split())

    S = 2 * N
    T = 2 * N + 1
    size = 2 * N + 2
    adj_list = [[] for _ in range(size)]

    for v in range(N):
        cap = 2 if (v == 0 or v == N-1) else 1
        add_edge(adj_list, v, v + N, cap, 0)

    for _ in range(M):
        u, v, c = map(int, input().split())
        u -= 1; v -= 1
        add_edge(adj_list, u + N, v, 1, c)

    add_edge(adj_list, S, 0,2, 0)
    add_edge(adj_list, N-1 + N, T, 2, 0)

    flow, cost = min_cost_max_flow(adj_list, S, T)
    print(cost)



