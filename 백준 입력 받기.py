#정수형 입력 띄어쓰기로 구분 1 5
a,b = map(int,input().split())

#정수형 입력(띄어쓰기로 구분) 5 1 2 1 1 1
arr = list(map(int,input().split()))

#1차원 배열
#정수형 입력(띄어쓰기로 구분,N값이 있을 때)
arr = []
for i in range(n):
	arr.append(int(input()))
#정수형 입력 (엔터로 구분,n값이 엔터 횟수가 되야합니다.)
arr = [int(input()) for _ in range(n)]
#문자열 입력 (엔터로 구분,배열 속에 문자열 하나하나가 값으로 입력됩니다.)
arr = [input() for _ in range(i)]

#2차원 배열
#띄어쓰기 구분 X (한 숫자 다 값으로)
arr = [list(map(int,input())) for _ in range(n)]
#띄어쓰기로 구분 O
arr = [list(map(int,input().split())) for _ in range(n)]

