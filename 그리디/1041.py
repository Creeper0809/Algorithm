# 아래 주석은 알고리즘 설명
"""
주사위 전개도
 D
EABF
 C
일때 가능한 2면은 마주보는것 제외 전부 다 가능
(A,F),(D,C),(B,E) <- 불가능
3면은
(A,D,E),(A,C,E),(A,B,D),(A,B,C),(F,D,E),(F,C,E),(F,B,D),(F,B,C) <- 가능

쌓았을때
꼭짓점 = 3면의 합이 제일 적은 주사위 면
모서리 = 2면의 합이 제일 적은 주사위 면
꼭짓점, 모서리 제외 부분 = 제일 작은 면
일때가 합의 최소

꼭짓점(3면이 보이는 주사위)의 개수는
N = 1
꼭짓점 1개
N = 2
꼭짓점 4개
N = 3
꼭짓점 4개

즉 2개 이상일땐 꼭짓점 4개 고정
33
면(1면이 보이는 주사위)의 개수는
N = 1
면 0개
N = 2
면 0개
N = 3
4(면의 개수) X 2(주사위 개수) + 1(면의 개수) *X1(주사위 개수)
N = 4
4 X(2^2+2) 1 X 2^2
N = 5
4 X (3^2 + 3) + 3^3

= 4X((n-2)^2 + (n-2)) + (n-2)^2
= 5(n-2)^2 + 4(n-2)

모서리(2면이 보이는 주사위)의 개수는
N = 1
면 0개
N = 2
면 4개
N = 3
4 * 2 + 4 * 1
N = 4
4 * 3 + 4 * 2
= 4X(n-1) + 4X(n-2)

꼭짓점 개수 X 3면 합의 최소 + 모서리 개수 X 2면 합의 최소 + 면 개수 X 1면 합의 최소 = 답

N이 1일때는 좀 예외 눈치가 없어서 주사위의 가장 큰 부분을 안보이게 가리면 답
"""
n = int(input())
dice = list(map(int, input().split()))
answer = 0
if n == 1:
    answer = sum(dice) - max(dice)
    print(answer)
else:
    # 면 개수
    count = ((n - 2) ** 2) * 5 + 4 * (n - 2)
    answer += min(dice) * count
    # 모서리 개수
    count = (n-2)*4 + (n-1)*4
    # 2면의 최소 합 구하기
    impossible = [(0, 5), (5, 0), (1, 4), (4, 1), (2, 3), (3, 2)]
    temp = []
    for i in range(6):
        for j in range(6):
            if i != j and (i, j) not in impossible:
                temp.append(dice[i] + dice[j])
    minVal = min(temp)
    # 모서리 개수 * 2면의 최소 값
    answer += count * minVal
    # 꼭짓점의 수는 4
    # 3면의 최소 합 구하기
    possible = [(0, 3, 4), (0, 2, 4), (0, 1, 3), (0, 1, 2), (5, 3, 4), (5, 2, 4), (5, 1, 3), (5, 1, 2)]
    temp = []
    for i in possible:
        a, b, c = i
        temp.append(dice[a] + dice[b] + dice[c])
    minVal = min(temp)
    # 꼭짓점 개수 * 3면의 최소 값
    answer += minVal * 4
    print(answer)
