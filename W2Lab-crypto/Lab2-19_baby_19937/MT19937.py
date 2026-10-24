class MT19937:
    def __init__(self, seed):
        self.n = 624
        self.m = 397

        self.mt = [0] * self.n
        self.index = self.n

        self.mt[0] = seed & 0xffffffff

        for i in range(1, self.n):
            self.mt[i] = (
                0x6c078965 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i
            ) & 0xffffffff

    def twist(self):
        for i in range(self.n):
            x = ( (self.mt[i] & 0x80000000) | (self.mt[(i + 1) % self.n] & 0x7fffffff) )

            xA = x >> 1
            if x & 1:
                xA ^= 0x9908b0df

            self.mt[i] = self.mt[(i + self.m) % self.n] ^ xA

        self.index = 0

    def rand(self):
        if self.index >= self.n:
            self.twist()

        y = self.mt[self.index]
        self.index += 1

        # tempering
        y ^= y >> 11
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        y ^= y >> 18

        return y & 0xffffffff



