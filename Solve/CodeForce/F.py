#!/usr/bin/env pypy3
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()
        tt = input().strip()

        # collect invariants for s and t
        inv_s = []
        inv_t = []
        p = 1
        # for each power-of-two divisor p of n
        while p <= n:
            if n % p == 0:
                # compute XOR by residue mod p
                # we can reuse a single array of length p
                xr_s = [0]*p
                xr_t = [0]*p
                for i, ch in enumerate(s):
                    if ch == '1':
                        xr_s[i % p] ^= 1
                for i, ch in enumerate(tt):
                    if ch == '1':
                        xr_t[i % p] ^= 1
                # append the tuple of p invariants
                inv_s.append(tuple(xr_s))
                inv_t.append(tuple(xr_t))
            p <<= 1

        # compare all levels
        out.append("Yes" if inv_s == inv_t else "No")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
