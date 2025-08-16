t = int(input())
for _ in range(t):
    n,k = map(int,input().split())
    A = list(map(int,input().split()))
    sorted_a = sorted(A,reverse=True)
    B = sorted(list(map(int, input().split())),reverse=True)
    visited = [False] * n
    answer_temp = [0] * n
    for i in range(n):
        answer_temp["여기에 원래 sorted_a[i]의 A 인덱스"] = B[i]
    print(*answer_temp,sep=" ")