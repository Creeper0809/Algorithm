minn, maxx = map(int,input().split())
factorization = {}

for i in range(2,int(maxx**0.5)+1):
    d = max(1,int(minn/(i*i)))
    d *= i*i
    while d<=maxx:
        factorization[d] = factorization.get(d,False)
        d+=i*i

result = 0
for i in range(minn,maxx+1):
    if factorization.get(i,True):
        result+=1
print(result)