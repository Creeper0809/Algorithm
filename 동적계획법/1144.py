import sys

input = sys.stdin.readline

INF = 10**9 + 7

def norm(s):
    mapping = {}
    t = 1
    for c in s:
        if c != '0' and c not in mapping:
            mapping[c] = str(t)
            t += 1
    ret = ''.join(mapping.get(c, '0') if c != '0' else '0' for c in s)
    return ret

def merge(s):
    ret = s[1:]
    if s[0] == '0' and s[-1] == '0':
        ret += '9'
    elif s[0] == '0':
        ret += s[-1]
    elif s[-1] == '0' or s[0] == s[-1]:
        ret += s[0]
    else:
        ret += s[0]
        ret = ret.replace(s[-1], s[0])
    return norm(ret)

def merge2(s):
    ret = s[1:]
    if s[0] == '0':
        ret += '9'
    else:
        ret += s[0]
    return norm(ret)

def check_pass(s):
    if s[0] == '0':
        return True
    return s[0] in s[1:]

def check_valid(s):
    unique_digits = {c for c in s if c != '0'}
    return len(unique_digits) <= 1

def dfs(x, y, cur, v, cache, n, m):
    if x == n:
        return 0 if check_valid(cur) else INF
    cur = norm(cur)
    if cur in cache[x][y]:
        return cache[x][y][cur]
    ret = INF
    nx = x
    ny = y + 1
    if ny >= m:
        nx += 1
        ny = 0
    if check_pass(cur):
        nxt = cur[1:] + '0'
        ret = min(ret, dfs(nx, ny, nxt, v, cache, n, m))
    next_cur = merge(cur) if y else merge2(cur)
    cost = dfs(nx, ny, next_cur, v, cache, n, m) + v[x][y]
    ret = min(ret, cost)
    if check_valid(cur):
        ret = min(ret, 0)
    cache[x][y][cur] = ret
    return ret

n, m = map(int, input().split())
v = [list(map(int, input().split())) for _ in range(n)]

cache = [[{} for _ in range(m)] for _ in range(n)]
print(dfs(0, 0, '0' * m, v, cache, n, m))