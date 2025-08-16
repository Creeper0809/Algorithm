import sys

N,M = map(int,sys.stdin.readline().rstrip().split())
dictpoke = dict()
for i in range(1,N+1):
    poke = sys.stdin.readline().rstrip()
    dictpoke[str(i)] = poke
    dictpoke[poke] = i

for _ in range(M):
    inputs = sys.stdin.readline().rstrip()
    print(dictpoke[inputs])