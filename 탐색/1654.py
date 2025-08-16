K, N = map(int, input().split())
wires = [int(input()) for _ in range(K)]
lo,hi = 0, max(wires) + 1

while lo + 1 <hi:
    mid = (lo+hi)//2
    if sum(wire // mid for wire in wires) >= N:
        lo = mid
    else:
        hi = mid

print(lo)