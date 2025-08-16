import sys

input = sys.stdin.readline
print = sys.stdout.write


N,M = map(int,input().rstrip().split())
dict = dict()
for _ in range(N):
    site,password = input().rstrip().split()
    dict[site] = password
for _ in range(M):
    site = input().rstrip()
    print(dict.get(site)+'\n')
