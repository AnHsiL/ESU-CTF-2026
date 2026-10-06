from pwn import *
from sympy import Matrix

HOST = "45.77.20.255" 
PORT = "31017"

p = 2**255 - 19
a, b = 0xdeadbeefcafebabe123456789abcdef0, 0

def lcg(x):
    return (a*x + b) % p


r = remote(HOST, PORT)

hide_bit = 192
known = []

# X1 = (K1 << hide_bit) + e1
for _ in range(16):
    r.sendlineafter(b"> ", b"next")
    r.recvuntil(b"now: ")
    known.append(int(r.recvline().strip()))

# ------------------------
#
# 建立 Lattice & 執行 LLL
#
# ------------------------

hide = 1 << hide_bit        # e 的數值上限 -> 0 < e_i < hide = 2^192
n = 8                       # 一次用 8 組輸出建立 Lattice

ai = [pow(a, i, p) for i in range(n)]
# e_i = a^i*e_0 + offsets
offsets = [ (ai[i]*known[0]*hide - known[i]*hide) % p for i in range(n) ]

# 建立 Lattice
basis = [ai + [0]]
for i in range(1, n):
    row = [0] * (n+1)
    row[i] = p
    basis.append(row)

basis.append(offsets + [hide])

# LLL reduced
reduced = Matrix(basis).lll()

# ------------------------
#
# 還原 X1
#
# ------------------------

X1 = None

for row in reduced.tolist():
    row = [int(x) for x in row]

    if abs(row[-1]) != hide:
        continue

    if row[-1] < 0:
        row = [-x for x in row]

    # 低 192 bits 必須在合法範圍
    if not all(0 <= x < hide for x in row[:-1]):
        continue

    candidate = (known[0] << hide_bit) + row[0]

    if all(
        ((candidate * pow(a, i, p)) % p) >> hide_bit == y
        for i, y in enumerate(known)
    ):
        X1 = candidate
        break

if X1 is None:
    raise ValueError("無法還原 X1")

print("X1 =", X1)

cur = X1
for _ in range(16):
    cur = lcg(cur)

r.sendlineafter(b"ans: ", str(cur).encode())

print(r.recvall().decode())