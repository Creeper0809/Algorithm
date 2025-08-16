(N,score,p) = map(int,input().split())
leaderboard = []
if N != 0:
    leaderboard = list(map(int,input().split()))
def solution():
    if N==p and leaderboard[-1]>=score:
        return -1
    rank = 1
    for i in leaderboard:
        if i>score:
            rank += 1
        else:
            break
    return rank
print(solution())