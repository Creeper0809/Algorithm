import math

N = int(input())
color = input()
weight = list(map(int, input().split()))

now_color = color[0]
max_weight = weight[0]

stones = list()
for i in range(1,N):
    if color[i] != now_color:
        stones.append(max_weight)
        max_weight = weight[i]
        now_color = color[i]
    else:
        max_weight = max(max_weight,weight[i])
stones.append(max_weight)

sorted_arr = sorted(stones[1:len(stones)-1],reverse=True)
answer = 0
for i in range(math.ceil(len(sorted_arr)/2)):
    answer += sorted_arr[i]
print(answer)

