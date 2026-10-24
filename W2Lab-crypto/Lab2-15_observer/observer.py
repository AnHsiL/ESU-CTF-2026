from pwn import *
from itertools import product
import HashTools

HOST = "45.77.20.255"
PORT = "31011"

r = remote(HOST, PORT)
r.recvuntil(b'gift!\n')
p_flag = r.recvline().decode()

prefix = p_flag.split(" ")[0]
flag_len = int(p_flag.split(" ")[1])

flag = [None] * flag_len
for i, c in enumerate(prefix.encode()):
    flag[i] = c
flag[-1] = ord("}")

CHARSET = b"0123456789abcdef" # hex
BLOCK_LEN = 64  # MD5 Block = 64 bytes
PAD_LEN = 9  # MD5 padding 最短 9 bytes 

def oracle(msg):
    r.sendlineafter(b"> ", msg.hex().encode())
    return r.recvline().decode().split("<", 1)[1].strip()

while None in flag:
    best = None
    for k in range(flag_len + 1):
        msg_len = (BLOCK_LEN - PAD_LEN) + BLOCK_LEN*k
        if msg_len < flag_len:
            continue

        positions = [(msg_len + i) % flag_len for i in range(PAD_LEN)]
        to_guess = sorted({pos for pos in positions if flag[pos] is None})

        if not to_guess:
            continue

        if best is None or len(to_guess) < len(best[1]):
            best = (msg_len, to_guess)

    if best is None:
        raise RuntimeError("找不到可用的 padding 位置")

    msg_len, to_guess = best
    if len(to_guess) > 2:
        raise RuntimeError("需同時猜過多 bytes")
    
    msg = b"\x00" * msg_len
    md5 = oracle(msg)
    new_MD5 = HashTools.new("md5")
    new_msg, sign = new_MD5.extension(
        secret_length=0,
        original_data=msg,
        append_data=b"",
        signature=md5
    )
    padding = new_msg[msg_len:]

    found = False
    for guess in product(CHARSET, repeat=len(to_guess)):
        guess_map = dict(zip(to_guess, guess))

        xor_pad = bytes(
            padding[i] ^ (
                flag[(msg_len + i) % flag_len]
                if flag[(msg_len + i) % flag_len] is not None
                else guess_map[(msg_len + i) % flag_len]
            )
            for i in range(len(padding))
        )

        if oracle(msg + xor_pad) == sign:
            for pos, value in guess_map.items():
                flag[pos] = value

            print(bytes(c if c is not None else ord("-") for c in flag).decode())

            found = True
            break

    if not found:
        raise RuntimeError("找不到匹配值")

print("="*30)
print("flag =", bytes(flag).decode())