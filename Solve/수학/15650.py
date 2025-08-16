import itertools

N,M = map(int,input().split())

number = set([i for i in range(1,N+1)])

for comb in itertools.combinations(number,M):
    print(" ".join(map(str,sorted(list(comb)))))
