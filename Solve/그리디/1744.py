N = int(input())
arr = [int(input()) for _ in range(N)]
arr.sort()
posit  = []
nega = []
answer = 0
haszero = False
for i in arr:
    if i<0:
        nega.append(i)
    elif i == 1:
       answer += 1
    elif i == 0:
        haszero = True
    else:
        posit.append(i)
if len(nega) % 2 != 0:
    if haszero:
        nega.pop()
    else:
        answer += nega.pop()
for i in range(0,len(nega)-1,2):
    answer += nega[i] * nega[i+1]
if len(posit) % 2 != 0:
    answer += posit.pop(0)
for i in range(0,len(posit)-1,2):
    answer += posit[i] * posit[i+1]
print(answer)

