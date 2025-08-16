k = int(input())
a,b,c,d = map(int,input().split())

if (a*k) + b != (c*k) + d:
    print("No")
else:
    print(f"Yes {(a*k) + b}")