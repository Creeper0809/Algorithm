"""
준현이는 주식을 살 수만 있다면 무조건 구매
성민이는 3일 연속 하락장(전날과 오늘이 같으면 하락으로 취급 X)이면 전량 구매/ 3일 연속 상승장이면 전량 구매

그냥 사고 팔고 성민이한테만 예외적으로 하나의 룰을 적용해서 사고팔게하면 되는 간단한 문제였다.

예제 입력
100
10 20 23 34 55 30 22 19 12 45 23 44 34 38
"""

money = int(input())
stock = list(map(int, input().split()))
status = {}


def buy(who, nowDay):
    money = status[who][0]
    if money < stock[nowDay]:
        return

    status[who][1] += money // stock[nowDay]
    status[who][0] = money % stock[nowDay]


def sell(who, nowDay):
    if status[who][1] == 0:
        return
    status[who][0] += status[who][1] * stock[nowDay]
    status[who][1] = 0


def buyOrSellByRule(who, nowDay):
    if nowDay < 2:
        return
    if stock[nowDay-2] < stock[nowDay-3] and stock[nowDay-1] < stock[nowDay-2]:
        buy(who,nowDay)
    elif stock[nowDay-2] > stock[nowDay-3] and stock[nowDay-1] > stock[nowDay-2]:
        sell(who,nowDay)

# 각자 돈 부여
status["준현"] = [money, 0]
status["성민"] = [money, 0]

# 주식 시작
for i in range(13):
    buy("준현",i)                 # 준현이는 신경 쓸 필요도 없이 계속 사게 만든다
    buyOrSellByRule("성민",i)     # 성민이는 특별한 룰을 적용해 사고 팔게 한다

# 총 자산
sell("준현", 13)
sell("성민", 13)

#답 출력
if status["준현"][0] > status["성민"][0]:
    print("BNP")
elif status["준현"][0] < status["성민"][0]:
    print("TIMING")
else:
    print("SAMESAME")
