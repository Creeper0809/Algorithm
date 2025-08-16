import sys
input = sys.stdin.readline

n = int(input())
initial_values = [0] + list(map(int, input().split()))
tree = [[0] * (4 * n), [0] * (4 * n)]

def range_update(l, r, value, start, end, node):
    if l == start and r == end:
        tree[0][node] += value
        tree[1][node] += 1
        return
    mid = (start + end) // 2
    if r <= mid:
        range_update(l, r, value, start, mid, node * 2)
    elif l > mid:
        range_update(l, r, value, mid + 1, end, node * 2 + 1)
    else:
        range_update(l, mid, value, start, mid, node * 2)
        range_update(mid + 1, r, value + mid + 1 - l, mid + 1, end, node * 2 + 1)

def point_query(index, start, end, node):
    global result
    result += tree[0][node] + tree[1][node] * (index - start)
    if start == end:
        return
    mid = (start + end) // 2
    if index <= mid:
        point_query(index, start, mid, node * 2)
    else:
        point_query(index, mid + 1, end, node * 2 + 1)

q = int(input())
for _ in range(q):
    query = list(map(int, input().split()))
    if query[0] == 1:
        l, r = query[1], query[2]
        range_update(l, r, 1, 1, n, 1)
    else:
        x = query[1]
        result = initial_values[x]
        point_query(x, 1, n, 1)
        print(result)