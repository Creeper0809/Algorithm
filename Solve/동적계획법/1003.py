import sys

fibo = {
    0: [0,1],
    1: [1,0]
}

def fibo_dynamic_programming(n, fibo_memo):
    if n in fibo_memo:
        return fibo_memo[n]
    fibo1 = fibo_dynamic_programming(n - 1, fibo_memo)
    fibo2 = fibo_dynamic_programming(n - 2, fibo_memo)
    arr = [0,0]
    arr[0] = fibo1[0] + fibo2[0]
    arr[1] = fibo1[1] + fibo2[1]
    fibo_memo[n] = arr
    return fibo_memo[n]


num = int(sys.stdin.readline())
a = [sys.stdin.readline().strip() for i in range(num)]
for i in a:
    fibomemo = fibo_dynamic_programming(int(i), fibo)
    print(fibomemo[1],fibomemo[0])
