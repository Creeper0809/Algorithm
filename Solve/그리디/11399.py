N = int(input())
arr = list(map(int,input().split()))

arr.sort()

answer = 0
temp = []
for i in arr:
    temp.append(i)
    answer += sum(temp)
print(answer)