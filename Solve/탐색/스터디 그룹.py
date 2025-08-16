N, K, D = map(int, input().split())
known_algo = [set() for _ in range(N)]
score = [0] * N
for j in range(N):
    m, d = map(int, input().split())
    score[j] = (d, j)
    for i in map(int, input().split()):
        known_algo[j].add(i)

l = r = 0
freq = {}
answer = -1

score.sort()

while r < N:
    student = score[r][1]
    for algo in known_algo[student]:
        freq[algo] = freq.get(algo, 0) + 1
    r+=1

    while l < r and score[r-1][0] - score[l][0] > D:
        student = score[l][1]
        for algo in known_algo[student]:
            freq[algo] -= 1
            if freq[algo] == 0:
                del freq[algo]
        l += 1
    answer = max(answer, (len(freq) - list(freq.values()).count(r-l)) * (r - l))

print(answer)
