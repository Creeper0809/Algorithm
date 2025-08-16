MOD = 998244353
PRIMITIVE_ROOT = 3

def modpow(x, e, m=MOD):
    r = 1
    while e:
        if e & 1:
            r = r * x % m
        x = x * x % m
        e >>= 1
    return r

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = modpow(PRIMITIVE_ROOT, (MOD - 1) // length)
        if invert:
            wlen = modpow(wlen, MOD - 2)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v + MOD) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = modpow(n, MOD - 2)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def ntt_convolution(a, b):
    n = 1
    while n < len(a) + len(b):
        n <<= 1
    a += [0] * (n - len(a))
    b += [0] * (n - len(b))

    ntt(a, False)
    ntt(b, False)
    for i in range(n):
        a[i] = a[i] * b[i] % MOD
    ntt(a, True)
    return a

number_size = int(1e6)
is_prime = [True] * (number_size + 1)
is_prime[0] = is_prime[1] = False
m = int(number_size ** 0.5)
for i in range(2, m + 1):
    if is_prime[i]:
        for j in range(i * i, number_size + 1, i):
            is_prime[j] = False

odd_prime = [0] * (number_size + 1)
semi_even_prime = [0] * (number_size + 1)
for p in range(2, number_size+1):
    if is_prime[p]:
        odd_prime[p] = 1
        if 2*p <= number_size:
            semi_even_prime[2*p] = 1

c = ntt_convolution(odd_prime[:], semi_even_prime[:])


n = int(input())
c_size = len(c)
for _ in range(n):
    k = int(input())
    print(c[k] if k < c_size else 0)


