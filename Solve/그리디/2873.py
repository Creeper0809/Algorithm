R,C = map(int,input().split())
rollerCoasterMap = list()
lowRow,lowColumn,lowNum = -1,-1,float('inf')

for i in range(R):
    temp = list(map(int,input().split()))
    for j in range(C):
        num = temp[j]
        if (j%2 == 0 and i % 2== 1) or (j%2 == 1 and i %2 == 0):
            if lowNum > num:
                lowNum = num
                lowRow = i
                lowColumn = j
    rollerCoasterMap.append(temp)

answer = ""

if  C % 2 == 1:
    answer = ('D' * (R - 1) + 'R' + 'U' * (R - 1) + 'R') * (C//2) + "D" *(R-1)
elif R % 2 == 1:
    answer = ('R' * (C - 1) + 'D' + 'L' * (C - 1) + 'D') * (R//2) + "R" * (C-1)
else:
    #print("특수조건 탐색")
    answer = ('D' * (R - 1) + 'R' + 'U' * (R - 1) + 'R') * (lowColumn // 2)
    c = 2*(lowColumn//2)
    bound = 2*(lowColumn//2) + 1
    r = 0
    while r != R-1 or c != bound:
        if c < bound and lowRow != r:
            c+= 1
            answer += "R"
        elif c == bound and lowRow != r:
            c -= 1
            answer += "L"
        if r != R-1:
            r+= 1
            answer += "D"

    answer += ('R' + 'U' * (R - 1) + 'R' + 'D' * (R - 1)) * ((C - lowColumn - 1) // 2)

#print(rollerCoasterMap)
#print(lowRow,lowColumn,lowNum)
print(answer)