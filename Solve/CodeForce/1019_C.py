import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    INF = 10**18
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        B = [1 if x <= k else -1 for x in a]
        P = [0]*(n+1)
        for i in range(1, n+1):
            P[i] = P[i-1] + B[i-1]
        S_total = P[n]
        nm = n & 1
        l_min = INF
        for i in range(1, n-1):
            if P[i] >= (i & 1):
                l_min = min(l_min, i)
        r_max = -INF
        for r in range(1, n):
            t3 = nm ^ (r & 1)
            if P[r] <= S_total - t3:
                r_max = max(r_max, r)
        if l_min < r_max:
            print("YES")
            continue
        maxEvenAt = [-INF]*(n+1)
        maxOddAt  = [-INF]*(n+1)
        for i in range(1, n):
            if   i & 1: maxOddAt[i]  = P[i]
            else:      maxEvenAt[i] = P[i]

        suffMaxEven = [-INF]*(n+2)
        suffMaxOdd  = [-INF]*(n+2)
        for i in range(n-2, 0, -1):
            suffMaxEven[i] = max(suffMaxEven[i+1], maxEvenAt[i+1])
            suffMaxOdd[i]  = max(suffMaxOdd[i+1],  maxOddAt[i+1])

        ok = False
        for l in range(1, n-1):
            if P[l] < (l & 1):
                continue
            if l & 1:
                if suffMaxOdd[l]  >= P[l]:       ok = True
                if suffMaxEven[l] >= P[l] + 1:   ok = True
            else:
                if suffMaxEven[l] >= P[l]:       ok = True
                if suffMaxOdd[l]  >= P[l] + 1:   ok = True
            if ok:
                print("YES")
                break
        if ok:
            continue
        prefMinEven = [INF]*(n+2)
        prefMinOdd  = [INF]*(n+2)
        for r in range(2, n+1):
            prefMinEven[r] = prefMinEven[r-1]
            prefMinOdd[r]  = prefMinOdd[r-1]
            if (r-1) & 1:
                prefMinOdd[r] = min(prefMinOdd[r], P[r-1])
            else:
                prefMinEven[r] = min(prefMinEven[r], P[r-1])

        for r in range(2, n):
            t3 = nm ^ (r & 1)
            if P[r] > S_total - t3:
                continue
            if r & 1:
                mRp  = prefMinOdd[r]
                mRdp = prefMinEven[r]
            else:
                mRp  = prefMinEven[r]
                mRdp = prefMinOdd[r]
            if mRp <= P[r]:
                ok = True
            if mRdp <= P[r] - 1:
                ok = True
            if ok:
                print("YES")
                break
        else:
            print("NO")

if __name__ == "__main__":
    solve()
