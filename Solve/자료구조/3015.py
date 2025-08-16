import sys
input = sys.stdin.readline

N = int(input())
stack = []
answer = 0

for _ in range(N):
    height = int(input())
    count = 1
    while stack and stack[-1][0] <= height:
        # 스택의 꼭대기 요소(이전에 본 사람의 키)가 현재 사람의 키보다 작거나 같다면,
        # 현재 사람은 그 사람들과 모두 볼 수 있다.
        if stack[-1][0] == height:
            # 만약 높이가 같은 경우라면, 이전에 같은 높이로 연속된 사람들의 개수를 합산한다.
            count += stack[-1][1]
        # 스택의 꼭대기 요소에 해당하는 사람들과의 쌍을 현재 사람이 형성하므로,
        # 그 사람들의 개수(stack[-1][1])만큼 answer에 더해준다.
        answer += stack[-1][1]
        # 현재 사람보다 작거나 같은 키인 사람들은 더 이상 이후에 현재 사람과 연결될 수 없으므로 pop한다.
        stack.pop()
    # while문 종료 후 스택에 남아 있다면,
    # 남아 있는 스택의 꼭대기는 현재 사람보다 큰 키를 갖고 있으므로,
    # 현재 사람은 그 사람과 한 쌍(즉, 양쪽에서 서로 볼 수 있는 관계)을 이룰 수 있다.
    if stack:
        answer += 1
    # 현재 사람을 (height, count) 형태로 스택에 push한다.
    # 여기서 count는 동일한 높이의 연속된 사람들을 하나의 그룹으로 처리하기 위해 사용된다.
    stack.append((height, count))
print(answer)
