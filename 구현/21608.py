import sys

input = sys.stdin.readline
N = int(input())
a = {}
dir = [[1,0],[-1,0],[0,1],[0,-1]]
classm = [[0]*N for _ in range(N)]
for i in range(N**2):
    nums = list(map(int,input().split()))
    studentNum = nums.pop(0)
    a[studentNum] = nums
    temp = []
    for n in range(N):
        for m in range(N):
            countBlank = 0
            countFav = 0
            if classm[n][m] != 0:
                continue
            for k in dir:
                if 0<=n+k[0]<N and 0<=m+k[1]<N:
                    if classm[n+k[0]][m+k[1]] in nums:
                        countFav += 1
                    elif classm[n+k[0]][m+k[1]] == 0:
                        countBlank += 1
            temp.append((n,m,countFav,countBlank))
    temp.sort(reverse=True,key=lambda x:(x[2],x[3],-x[0],-x[1]))
    classm[temp[0][0]][temp[0][1]] = studentNum
answer = 0
for n in range(N):
    for m in range(N):
        studentnum = classm[n][m]
        count = 0
        for k in dir:
            if 0 <= n + k[0] < N and 0 <= m + k[1] < N:
                if classm[n+k[0]][m+k[1]] in a[studentnum]:
                    count+=1
        if count != 0:
            answer += 10**(count-1)
print(answer)
