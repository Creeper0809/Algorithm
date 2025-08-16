import random

def unshiftRight(x, shift):
    res = x
    for i in range(32):
        res = x ^ (res >> shift)
    return res

def unshiftLeft(x, shift, mask):
    res = x
    for i in range(32):
        res = x ^ ((res << shift) & mask)
    return res

def untemper(v):
    v = unshiftRight(v, 18)
    v = unshiftLeft(v, 15, 0xefc60000)
    v = unshiftLeft(v, 7, 0x9d2c5680)
    v = unshiftRight(v, 11)
    return v

original = random.Random(12345)
outputs = [original.getrandbits(32) for _ in range(624)]

recovered_state = [untemper(out) for out in outputs]

class MT19937:
    def __init__(self, state):
        self.state = state
        self.index = 624

    def twist(self):
        for i in range(624):
            y = (self.state[i] & 0x80000000) + (self.state[(i + 1) % 624] & 0x7fffffff)
            next_val = self.state[(i + 397) % 624] ^ (y >> 1)
            if y % 2:
                next_val ^= 0x9908b0df
            self.state[i] = next_val

    def getrandbits(self, bits=32):
        if self.index == 624:
            self.twist()
            self.index = 0
        y = self.state[self.index]
        self.index += 1
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        y ^= (y >> 18)
        return y & ((1 << bits) - 1)

recovered_rng = MT19937(recovered_state)

print(original.getrandbits(32) == recovered_rng.getrandbits(32))