N = list(input())
isReverse = True
temp2 = []
answer = ""
for i in N:
    if i == "<":
        isReverse = False
        while temp2:
            answer+=temp2.pop()
        answer += "<"
    elif i == ">":
        answer+=">"
        isReverse = True
    elif i == " ":
        while temp2:
            answer+=temp2.pop()
        answer+=i
    elif isReverse:
        temp2.append(i)
    else:
        answer+=i
while temp2:
    answer +=temp2.pop()
print(answer)