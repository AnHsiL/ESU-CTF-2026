
from pwn import *
from MT19937 import MT19937

MASK32 = 0xffffffff


def rotateR(y, shift, mask=MASK32):
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


def init_mt(states):
    MT = MT19937(0)
    MT.mt = states.copy()
    MT.index = 624
    return MT


# GF(2) Gaussian elimination
def solve_gf2(equations, n):
    pivots = {}

    for mask, rhs in equations:
        while mask:
            bit = (mask & -mask).bit_length() - 1

            if bit in pivots:
                old_mask, old_rhs = pivots[bit]
                mask ^= old_mask
                rhs ^= old_rhs
            else:
                pivots[bit] = (mask, rhs)
                break

        if mask == 0 and rhs:
            raise ValueError("Inconsistent equations")

    if len(pivots) < n:
        raise ValueError(
            f"Insufficient rank: {len(pivots)}/{n}"
        )

    solution = 0

    # 最低位元作為 pivot，必須從高位元往低位元回代
    for bit in sorted(pivots, reverse=True):
        mask, rhs = pivots[bit]

        other = mask ^ (1 << bit)
        value = rhs ^ ((other & solution).bit_count() & 1)

        if value:
            solution |= 1 << bit

    return solution



OUTPUT_BITS = 1337
OUTPUT_NUM = OUTPUT_BITS // 32  # 41
LAST_BITS = OUTPUT_BITS % 32    # 25
ROUNDS = 30  # 15 次理論上已足夠，但方程式不一定線性獨立 -> 保守 30


HOST = "45.77.20.255" 
PORT = "31019"

r = remote(HOST, PORT)

outputs = []
masks = []

for _ in range(ROUNDS):
    r.sendlineafter(b"> ", b"next")
    value = int(r.recvline().decode().split(": ", 1)[1])

    # 41 個 32-bit chunks
    for i in range(OUTPUT_NUM):
        outputs.append((value >> (32 * i)) & MASK32)
        masks.append(MASK32)

    # ...25 bits
    last_25 = ( value >> (32 * OUTPUT_NUM) ) & ((1 << LAST_BITS) - 1)

    outputs.append(last_25 << 7)
    masks.append(MASK32 ^ 0x7f)

states = [untemper(out) for out in outputs[:624]]

unknown = []
for i in range(624):
    if masks[i] != MASK32:
        for bit in range(7):
            unknown.append((i, bit))


count = len(outputs) - 624

MT = init_mt(states)
base = [MT.rand() for _ in range(count)]


# 未知 bit 的影響
effects = []
for pos, bit in unknown:
    test_states = states.copy()
    test_states[pos] ^= untemper(1 << bit)

    MT_test = init_mt(test_states)

    effect = [  MT_test.rand() ^ base[i]  for i in range(count) ]
    effects.append(effect)


# 建立 GF(2) 線性方程組，求解未知 bits
equations = []
for i in range(count):
    target = outputs[624 + i]
    mask = masks[624 + i]

    diff = (target ^ base[i]) & mask

    for bit in range(32):
        if not (mask & (1 << bit)):
            continue

        row = 0
        for j in range(len(unknown)):
            if effects[j][i] & (1 << bit):
                row |= 1 << j

        rhs = (diff >> bit) & 1
        equations.append((row, rhs))


solution = solve_gf2(equations, len(unknown))

for j, (pos, bit) in enumerate(unknown):
    if solution & (1 << j):
        states[pos] ^= untemper(1 << bit)


# 驗證恢復結果
MT = init_mt(states)

for i in range(count):
    predicted = MT.rand()
    actual = outputs[624 + i]
    mask = masks[624 + i]

    assert (predicted & mask) == actual, (
        f"Mismatch at output {624 + i}"
    )

ans = 0
for i in range(OUTPUT_NUM):
    ans |= MT.rand() << (32 * i)

ans |= (MT.rand() >> 7) << (32 * OUTPUT_NUM)


r.sendlineafter(b"> ", b"ans")
r.sendlineafter(b"ans: ", str(ans).encode())

print(r.recvall(timeout=3).decode(errors="replace"))
