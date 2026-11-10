from Crypto.Util.number import *
from pwn import *
from fractions import Fraction
import math

HOST = "45.77.20.255"
PORT = "31009"

r = remote(HOST, PORT)

N = int(r.recvline().decode().split('=')[1])
c = int(r.recvline().decode().split('=')[1])
e = 0x10001

multiplier = pow(2, e, N)

L = Fraction(0)
R = Fraction(N)

for _ in range(N.bit_length()):  # bit_length() = floor(log2(N))+1
    c = c * multiplier % N
    r.sendlineafter("> ", str(c).encode())
    isOdd = int(r.recvline().decode().split('< ')[1])
    mid = (L + R) / 2

    if isOdd:
        L = mid
    else:
        R = mid

print(long_to_bytes(int(R)))
