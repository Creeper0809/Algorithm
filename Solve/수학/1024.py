n,l = map(int,input().split())
x = -1
num = 0
for i in range(l,101):
    t = (i*i - i)/2
    if (n-t)%i == 0 and (n-t)//i>-1:
        x = (n-t)//i
        num = i
        break
if x == -1:
    print(-1)
else:
    for i in range(num):
        print(int(x + i),end=" ")