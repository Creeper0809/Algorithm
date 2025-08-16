while True:
    a,b,c = map(int,input().split())
    if a == b == c == 0:
        break
    arr = sorted([a,b,c])
    print("right" if arr[0]**2 + arr[1]**2 == arr[2]**2 else "wrong")