"""
보통 x y에 대치되게 열 행으로 주는데 여기는 행 열로 줘서 입력이 헷갈렸다. 이 문제의 핵심은 탱크끼리 행도 열도 겹치는게 있으면 안된다.
xxxxx   xoooo
ooooo   oxooo
ooooo ->ooxoo
ooooo   oooxo
ooooo   oooox
(1,1),(2,1),(3,1)(4,1),(5,1) 이렇게 존재한다면 행은 겹치는 숫자가 없으니 잘 맞춘것이다.
열은 모든 숫자가 다 겹치기 떄문에 1~5까지 다시 재 배치를 해줘야한다
(1,1),(2,2),(3,3)(4,4),(5,5)
이게 제대로 된 배치

제대로 된 배치가 되려면 행과 열에 겹치는게 있으면 안된다는걸 알았으니 움직임을 최소로 하는 방법을 생각해야한다.
움직임을 최소로 하려면 1~N까지 배치 할때 가장 가까운 거리에 있는 탱크가 움직이는게 제일 좋다
만약
ooooo   xoooo
oxxoo   oxooo
ooxoo ->ooxoo
ooxxo   oooxo
ooooo   oooox
탱크를 (2,2)(3,3),(2,3),(4,4)(3,4),에 배치 한다고 가정해보자
먼저 행을 정리를 하면
2 3 2 4 3
이다
0~N까지에 배치를 해야 하기때문에 0부터 배치를 한다고 가정해보면
0은 거리가 2인 탱크들이 가야 최소가 된다 그래서 2 두개중 하나를 0에 배치 한다 0 3 2 4 3 -> UP 두번
1은 거리가 2인 탱크가 가야 최소가 될 것이다 그래서 남은 2 하나를 1에 배치한다 0 3 1 4 3 -> UP 한번
2는 거리가 3인 탱크가 가야 최소가 된다 그래서 3중 하나를 2에 배치한다 0 2 1 4 3 -> UP한번
3은 거리가 3인 탱크가 존재하니 냅둔다
4는 거리가 4인 탱크가 존재하니 냅둔다
5는 남은 탱크가 움직이면 된다 -> DOWN 두번

열도 똑같이 이런식으로 정리를 했을 때 최소가 된다

나는 여기까지만 생각을 해서 첫 시도에 틀렸다. 그 이유는 디버그를 해보니 11333일때가 문제였다
만약 11333을 인덱스에 맞춰 정리를 한다면 4까지는 문제가 생기지 않지만 5번쨰를 정리할때 4를 거쳐가기때문에 "탱크는 겹칠일이 없다"라는 조건에 위배를 하게 됐다.
이걸 해결하기위해서 i보다 c가 작을때 i보다 c가 클때로 나눠서 클때는 역순으로 정렬을 해주고 작을떄는 원래 순서대로 정렬을 해주면 될 것 같다.

두번째 시도는 시간제한에 걸렸다
이유는 쓸모 없는 while문을 사용해서 그런듯 하다
    while Tanks[i].x < i:
        answer += (str(Tanks[i].tanknum) + " D\n")
        Tanks[i].x += 1
        totalMove += 1
이 부분은 굳이 while문으로 돌릴 필요가 없이 그냥 바로 계산 i와 현재 위치의 차이를 바로 넣어주는거로 계산이 가능 할 것 같아
    if Tanks[i].x < i:
        answer += (str(Tanks[i].tanknum) + " D\n")*(i - Tanks[i].x)
        totalMove += i - Tanks[i].x
        Tanks[i].x = i
로 대체 했다 그랬더니 시간제한도 걸리지 않고 문제도 통과가 가능했다.
"""
import sys


class Tank:
    x = 0
    y = 0
    tanknum = 0

    def __init__(self, num1, num2, num3):
        self.x = num1
        self.y = num2
        self.tanknum = num3

    # 디버그용
    def __str__(self):
        return "탱크번호: " + str(self.tanknum) + " 행: " + str(self.x) + " 열: " + str(self.y)


N = int(sys.stdin.readline())
totalMove = 0
answer = ""
# 탱크들 추가
Tanks = []
for i in range(N):
    (x, y) = list(map(int, sys.stdin.readline().split()))
    Tanks.append(Tank(x - 1, y - 1, i + 1))
# 행을 기준으로 오름차순 정렬
Tanks.sort(key=lambda _: _.c)
for i in range(N):
    if Tanks[i].x > i:
        answer += (str(Tanks[i].tanknum) + " U\n") * (Tanks[i].x - i)
        totalMove += Tanks[i].x - i
        Tanks[i].x = i
for i in range(N - 1, -1, -1):
    if Tanks[i].x < i:
        answer += (str(Tanks[i].tanknum) + " D\n") * (i - Tanks[i].x)
        totalMove += i - Tanks[i].x
        Tanks[i].x = i
Tanks.sort(key=lambda _: _.query_r)
for i in range(N):
    if Tanks[i].y > i:
        answer += (str(Tanks[i].tanknum) + " L\n") * (Tanks[i].y - i)
        totalMove += Tanks[i].y - i
        Tanks[i].y = i
for i in range(N - 1, -1, -1):
    if Tanks[i].y < i:
        answer += (str(Tanks[i].tanknum) + " R\n") * (i - Tanks[i].y)
        totalMove += i - Tanks[i].y
        Tanks[i].y = i
print(str(totalMove) + "\n" + answer)
# 디버그 용
# Tanks.sort(key=lambda _: _.tanknum)
# for i in Tanks:
#    print(str(i))
