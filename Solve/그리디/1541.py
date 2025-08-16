num = input().split("-")
arr = []
for i in num:
    n = 0
    for j in i.split('+'):
        n += int(j)
    arr.append(n)
answer = arr[0]
for i in arr[1:]:
    answer -= i
print(answer)