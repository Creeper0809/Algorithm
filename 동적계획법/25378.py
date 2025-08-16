n = int(input())

stone_list = list(map(int, input().split()))
remain = [[i] for i in stone_list]
count = n

for i in range(1, n):
    for j in remain[i - 1]:
        if j < stone_list[i]:
            remain[i].append(stone_list[i] - j)
        if j == stone_list[i]:
            remain[i] = []
            count -= 1
            break
print(count)