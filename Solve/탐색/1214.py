D, P, Q = map(int, input().split())

if P < Q:
    P, Q = Q, P

ans = float('inf')
for k in range(Q):
    total = k * P
    if total >= D:
        ans = min(ans, total)
    else:
        remain = D - total
        q_need = (remain + Q - 1) // Q
        total2 = total + q_need * Q
        ans = min(ans, total2)

print(ans)
