import math

is_prime = [True for _ in range(3000)]
is_prime[0] = is_prime[1] = False

for i in range(2, int(math.sqrt(3000)) + 1):
    if not is_prime[i]:
        continue
    for j in range(i*i,3000,i):
        is_prime[j] = False

N = int(input())
nums = list(map(int, input().split()))

graph = {}

for i in range(N):
    graph[nums[i]] = []
    for j in range(N):
        if i != j and is_prime[nums[j] + nums[i]]:
            graph[nums[i]].append(nums[j])

def dfs(num,visited,matched,connected):
    if num in visited:
        return False
    visited.add(num)
    for i in graph[num]:
        if num in connected or i in connected:
            continue
        if matched[i] == - 1 or dfs(matched[i],visited,matched,connected):
            matched[i] = num
            return True
    return False

answer = []
def solve():
    for connected in graph[nums[0]]:
        matched = [-1] * 1001
        flow = 0
        for i in range(1,N):
            if nums[i] == connected:
                continue
            visited = set()
            if dfs(nums[i],visited,matched,(nums[0],connected)):
                flow += 1
        if flow == N - 2:
            answer.append(connected)
solve()
if answer:
    print(*sorted(answer))
else:
    print(-1)