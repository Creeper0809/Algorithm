m = input()

weights = [1 if i % 2 == 0 else 3 for i in range(13)]
result = 0
idx = -1

for i in range(13):
    if m[i] == "*":
        idx = i
    else:
        result += int(m[i]) * weights[i]

for x in range(10):
    temp = result + x * weights[idx]
    if temp % 10 == 0:
        print(x)
        break
