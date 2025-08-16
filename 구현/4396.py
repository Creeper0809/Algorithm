"""
어려운게 없는 그냥 주변 검사로 폭탄 찾기
"""
N = int(input())
bomb = []
dir = [[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]
answer = [[]]
openedbomb = False

for i in range(N):
    bomb.append(list(input()))

def checkHowMany(pos):
    x, y = pos
    global openedbomb
    if not openedbomb and bomb[x][y] == "*":
        openedbomb = True
    count = 0
    # 각 방향대로 폭탄이 있는지 검사
    for i in dir:
        dx, dy = i
        nx = x + dx
        ny = y + dy
        if  0 <= nx < N and 0 <= ny < N:
            if bomb[nx][ny] == "*":
                count += 1
    return str(count)

#.이면 그냥 넣고 X면 주변 폭탄 검사
for i in range(N):
    strarr = list(input())
    for j in range(N):
        if strarr[j] == ".":
            answer[i].append(strarr[j])
        else:
            answer[i].append(checkHowMany([i, j]))
    answer.append([])

#폭탄을 건든적이 있다면 *로 대체
if openedbomb:
    for i in range(N):
        for j in range(N):
            if bomb[i][j] == "*":
                answer[i][j] = "*"
for i in answer:
    print(''.join(i))