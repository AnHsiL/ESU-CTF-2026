import os
from flags import flag5 as flag
from Crypto.Util.number import getPrime

p = 2**255 - 19
a, b = 0xdeadbeefcafebabe123456789abcdef0, 0

def lcg(x):
    return (a*x + b) % p

seed = int.from_bytes(os.urandom(32), 'little')
cur = lcg(seed)

for _ in range(16):
    if input("> ") != 'next':
        break
    print("now:", cur>>192)
    cur = lcg(cur)

if int(input("ans: ")) == cur:
    print(flag)

else:
    print("failed qwq")
