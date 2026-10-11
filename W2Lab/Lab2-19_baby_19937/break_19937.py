from pwn import *
from MT19937 import MT19937

MASK32 = 0xffffffff

def rotateR(y, shift, mask=MASK32):
    # MT19937 是 32-bit，反覆約 ceil(32 / shift) 次就能完全還原
    x = y
    for _ in range(32 // shift + 1):
        x = y ^ ((x >> shift) & mask)
    return x & MASK32

def rotateL(y, shift, mask):
    x = y
    for _ in range(32 // shift + 1):
        x = y ^ ((x << shift) & mask)
    return x & MASK32

def untemper(out):
    state = rotateR(out, 18)
    state = rotateL(state, 15, 0xefc60000)
    state = rotateL(state, 7, 0x9d2c5680)
    state = rotateR(state, 11)
    return state

HOST = "45.77.20.255" 
PORT = "31018"

r = remote(HOST, PORT)

outputs = []
# 每次產生 4 個 32-bit 輸出
for _ in range(156):
    r.sendlineafter(b"> ", b"next")
    value = int(r.recvline().decode().split(": ", 1)[1])

    for i in range(4):
        outputs.append((value >> (32 * i)) & MASK32)

states = [untemper(int(out)) for out in outputs]

MT = MT19937(0)
MT.mt = states.copy()

ans = 0
for i in range(4):
    ans |= MT.rand() << (32 * i)

r.sendlineafter(b"> ", b"ans")
r.sendlineafter(b"ans: ", str(ans).encode())
print(r.recvline().decode())
