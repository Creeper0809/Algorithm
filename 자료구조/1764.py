import sys
input = sys.stdin.readline
N, M = map(int, input().split())
dict = {}
for _ in range(N):
    s = input().rstrip()
    dict[s] = dict.get(s, 0) + 1
for _ in range(M):
    s = input().rstrip()
    dict[s] = dict.get(s, 0) + 1
answer = ""
count = 0
dict = sorted(dict.items(), key=lambda x: x[0])
for t, s in dict:
    if s == 2:
        count += 1
        answer += t + '\n'
print(count)
print(answer)