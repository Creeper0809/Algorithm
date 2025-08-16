N = int(input())
arr = list(map(int, input().split()))
T,P = map(int, input().split())

tshirt = 0
for i in range(len(arr)):
    temp = arr[i] // T
    tshirt += temp
    arr[i] -= T * temp
    if arr[i] > 0:
        tshirt += 1

print(tshirt)
print(N//P, N%P)