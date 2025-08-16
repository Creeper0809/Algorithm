import itertools

n1 = [list(map(int, input().split())) for _ in range(5)]
nums = list(itertools.chain.from_iterable([list(map(int, input().split())) for _ in range(5)]))
correct = [[False for _ in range(5)] for _ in range(5)]
def sol():
    for i in range(len(nums)):
        (x,y) = [(n, m) for n in range(5) for m in range(5) if n1[n][m] == nums[i]][0]
        correct[x][y] = True
        binggo = 0
        for j in correct:
            if j.count(True) == 5:
                binggo += 1
        for j in range(5):
            if [t[j] for t in correct].count(True) == 5:
                binggo += 1
        if correct[0][0] and correct[1][1] and correct[2][2] and correct[3][3] and correct[4][4]:
            binggo += 1
        if correct[4][0] and correct[3][1] and correct[2][2] and correct[1][3] and correct[0][4]:
            binggo += 1
        if binggo >2:
            return i + 1
print(sol())
