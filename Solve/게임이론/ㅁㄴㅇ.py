import sys

sys.setrecursionlimit(10**8)
answer = 0
def calculate_grundy_dp(n, memo, get_moves):
    global answer
    # 돌이 0개일 때의 그런디 수는 0
    if n == 0:
        return 0
    # memoization
    if n in memo:
        return memo[n]
    s = set()
    # 가능한 모든 행동에 대해 그런디 수를 계산하여 집합에 추가
    for move in get_moves:
        if n - move < 0:
            continue
        s.add(calculate_grundy_dp(n-move, memo, get_moves))
    grundy = 0
    # mex 함수를 계산하여 그런디 수를 결정
    while grundy in s:
        grundy += 1
    if grundy == 0:
        answer+= 1
    memo[n] = grundy
    return grundy


def get_all_grundy_states_dp(states, get_moves):
    memo = {} # memoization을 위한 빈 딕셔너리
    grundy_states = {} # 각 돌 무더기의 그런디 수를 저장할 빈 딕셔너리
    for state in states:
        # 각 돌 무더기의 그런디 수 계산하여 딕셔너리에 추가
        grundy_states[state] = calculate_grundy_dp(state, memo, get_moves)
    return grundy_states



M = int(input())
K = int(input())
move = list(map(int,input().split()))
calculate_grundy_dp(M,{},move)
print(answer)