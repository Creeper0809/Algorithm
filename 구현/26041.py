arr = input().split()
prefix = input()

answer = 0
for i in arr:
    if prefix != i and i.startswith(prefix):
        answer += 1
print(answer)