from pwn import *

p = 2**255 - 19
a, b = 0x120, 0x1337

def lcg(x):
    return (a*x + b) % p


HOST = "45.77.20.255" 
PORT = "31015"

r = remote(HOST, PORT)
r.recvuntil("now: ")

now = int(r.recvline().strip())

cur = f'{lcg(now)}'
r.sendlineafter("ans:", cur.encode())

print(r.recvline().decode())