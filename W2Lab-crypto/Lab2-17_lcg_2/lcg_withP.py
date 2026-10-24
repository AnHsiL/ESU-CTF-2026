import math
from pwn import *

HOST = "45.77.20.255" 
PORT = "31016"

r = remote(HOST, PORT)
r.sendlineafter("> ", b'next')
r.recvuntil(b"now: ")
p1 = int(r.recvline().strip())

r.sendlineafter("> ", b'next')
r.recvuntil(b"now: ")
p2 = int(r.recvline().strip())

r.sendlineafter("> ", b'next')
r.recvuntil(b"now: ")
p3 = int(r.recvline().strip())

a, b = 0x120, 0x1337
p = math.gcd(a*p1 + b - p2, a*p2 + b - p3)

def lcg(x):
    return (a*x + b) % p

cur = f'{lcg(p3)}'
r.sendlineafter(b"> ", b"stop")
r.sendlineafter("ans: ", cur.encode())

print(r.recvline().decode())