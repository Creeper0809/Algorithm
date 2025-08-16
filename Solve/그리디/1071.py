"""
이 문제는 학교 동아리 선배로부터 미리 한번 설명을 듣고 푼 문제라 완벽히 스스로의 아이디어로 푼 문제는 아니다.


문제 정렬 조건은
사전 순으로 앞서는것을 출력할것, A[i] +1 = A[i+1]인것이 없어야 할 것 두가지다
문제에서 가장 중요한것은 인접한 인덱스끼리 교환 가능하다는 조건이 없다는 것이다 이게 왜 중요한면
사전 순으로 정리하는 가장 편한 방법은 입력 받은 값에서 sort를 때려버리고 계산하면 더 편하기 때문이다
이 문제에서는 두가지 케이스가 있다
1.A[i]+1 = A[i+1]이 존재 한다
2.A[i]+1 = A[i+1]이 존재 하지 않는다
A[i]+1 = A[i+1]이 존재하지 않을 경우에는 그냥 정렬도 해놨겠다 편하게 출력하면 된다
문제는 존재 했을 때 발생한다
여기서도 두가지 케이스가 나뉜다
A[i] + 2 이상이 남은 리스트에 존재하는가
존재하면 A[i]+1과 순서를 바꾸는게 사전상 앞일것이고
존재하지 않는다면 A[i]+1과 A[i]를 바꿔야한다

첫번째 시도에서는 딱 여기까지 생각했다
여기서 내가 놓쳤던 점은 그냥 같은 숫자끼리 묶어서 한번에 처리했지만
그렇게 하면 3 3 4 1 2 2 3 0 같은 케이스에서 문제가 생겼다 
옳바른 답은  0 2 1 3 2 4 3 3 이지만
한번에 묶어서 처리 했기 때문에 0 2 2 1 4 3 3 3 로 사전순으로 앞선 결과가 나오지 않았다

카운터를 이용하여 개수를 세기로 했다
"""
"""
import itertools
from collections import Counter

N = int(input())
arr = list(map(int,input().split()))

counted_num = Counter(arr)
sorted_num = list(set(arr))
usednum = list()
answer = list()
while len(usednum) != len(sorted_num):
    for i in range(len(sorted_num)):
        temp = sorted_num[i]
        if temp in usednum:
            continue
        usednum.append(temp)
        if temp + 1 not in sorted_num or temp + 1 in usednum:
            answer.append([temp] * counted_num[temp])
        else:
            hasTwoUp = False
            for j in sorted_num[i+1:]:
                if temp + 2<=j and j not in usednum:
                    answer.append([temp] * counted_num[temp])
                    answer.append([j] * counted_num[j])
                    usednum.append(j)
                    hasTwoUp = True
                    break
            if not hasTwoUp:
               answer.append([temp + 1] * counted_num[temp+ 1])
               answer.append([temp] * counted_num[temp])
               usednum.append(j)
answer = list(itertools.chain.from_iterable(answer))
for i in answer:
    print(i, end=" ")
"""
"""
첫번째 시도에서는 딱 여기까지 생각했다
여기서 내가 놓쳤던 점은 그냥 같은 숫자끼리 묶어서 한번에 처리했지만
그렇게 하면 3 3 4 1 2 2 3 0 같은 케이스에서 문제가 생겼다 
옳바른 답은  0 2 1 3 2 4 3 3 이지만
한번에 묶어서 처리 했기 때문에 0 2 2 1 4 3 3 3 로 사전순으로 앞선 결과가 나오지 않았다

카운터를 더 이용해서 처리하기로 했다
한번에 묶어서 처리를 하는것이 아닌 개수를 한개씩 빼주면서 맞게 정렬하면 된다
"""
from collections import Counter

N = int(input())
arr = list(map(int,input().split()))

counted_num = Counter(arr)
sorted_num = sorted(arr)
usednum = list()
answer = list()
while len(answer) != N:
    for i in range(len(sorted_num)):
        temp = sorted_num[i]
        if counted_num[temp] == 0:
            continue
        if temp + 1 not in sorted_num or counted_num[temp+1] == 0:
            while counted_num[temp] != 0:
                answer.append(temp)
                counted_num[temp] -= 1
        else:
            hasTwoUp = False
            for j in sorted_num[i+1:]:
                if temp + 2<=j and counted_num[j] != 0:
                    while counted_num[temp] != 0:
                        answer.append(temp)
                        counted_num[temp] -= 1
                    answer.append(j)
                    counted_num[j] -= 1
                    hasTwoUp = True
                    break
            if not hasTwoUp:
               answer.append(temp + 1)
               counted_num[temp+1] -= 1
for i in answer:
    print(i, end=" ")

