N = int(input())
arr = [list(map(int, input().split())) for _ in range(N)]
result = []
for i in range(N):
    score = 1
    for j in range(N):
        if i == j:
            continue
        if arr[i][0] < arr[j][0] and arr[i][1] < arr[j][1]:
            score += 1
    result.append(score)
print(*result)