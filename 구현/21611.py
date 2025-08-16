"""
마법 수행 -> 구슬 이동 -> 완전 탐색 후 같은 구슬 4개 인접시 폭발 -> 구슬 이동 ->
"""
dir = ['', [0, -1], [0, 1], [-1, 0], [1, 0]]
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
N, M = list(map(int, input().split()))
fieldByLoc = [list(map(int, input().split())) for _ in range(N)]
fieldByNum = []
locToNum = {}
numToLoc = {}
magic = [list(map(int, input().split())) for _ in range(M)]
middle = [(N + 1) // 2 - 1, (N + 1) // 2 - 1]
answer = 0

def init():
    nowposx = middle[0]
    nowposy = middle[1]
    count = 0
    direction = 0
    i = 1
    while count < N ** 2 - 1:
        for _ in range(2):
            for _ in range(i):
                nowposx += dx[direction]
                nowposy += dy[direction]
                if 0 <= nowposx <= N and 0 <= nowposy <= N:
                    fieldByNum.append(fieldByLoc[nowposy][nowposx])
                    locToNum[(nowposx, nowposy)] = count
                    numToLoc[count] = (nowposx, nowposy)
                    count += 1
            direction = (direction + 1) % 4
        i += 1


def arrangement():
    global fieldByNum
    count = fieldByNum.count(-1)
    fieldByNum = [i for i in fieldByNum if i != -1]
    fieldByNum.extend([0]*count)

def useMagic(direction, howMany):
    nowposx = middle[0]
    nowposy = middle[1]
    for _ in range(howMany):
        nowposx += dir[direction][0]
        nowposy += dir[direction][1]
        num = locToNum[(nowposx, nowposy)]
        #score[fieldByNum[num]] += 1
        fieldByNum[num] = -1

def destroyByChain():
    global answer
    destroyed = False
    nowNum = 0
    count = 0

    for i in range(N ** 2-1):
        if nowNum != fieldByNum[i]:
            if count > 3:  # 체인 개수가 3 이상이면 폭파
                answer += count * nowNum
                for j in range(i - count, i):
                    fieldByNum[j] = -1
                destroyed = True
            nowNum = fieldByNum[i]
            count = 1
        else:
            count += 1
    return destroyed

def transformation():
    global fieldByNum
    temp = []
    nowNum = fieldByNum[0]
    count = 0
    for i in range(N ** 2 - 1):
        if nowNum != fieldByNum[i]:
            temp.append(count)
            temp.append(nowNum)
            nowNum = fieldByNum[i]
            count = 1
        else:
            count += 1
    for i in range(len(temp)):
        if i >=(N**2-1):
            break
        fieldByNum[i] = temp[i]

init()
for (i,j) in magic:
    useMagic(i,j)
    arrangement()
    while True:
        if not destroyByChain():
            break
        arrangement()
    transformation()
print(answer)
