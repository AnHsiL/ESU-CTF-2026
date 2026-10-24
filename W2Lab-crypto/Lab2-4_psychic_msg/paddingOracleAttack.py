from pwn import *

HOST = "45.77.20.255"
PORT = "31003"

r = remote(HOST, PORT)

r.recvuntil("Encrypted Flag:")
enc_flag = bytes.fromhex(r.recvline().decode().strip())

def oracle(data):
    r.recvuntil(b"Your Message (hex) >") # Your Message (hex) >
    r.sendline(data.hex().encode())
    
    res = r.recvline().decode()
    return "I got that message!" in res

BLOCK_SZ = 16

blocks = [
    enc_flag[i:i + BLOCK_SZ] for i in range(0, len(enc_flag), BLOCK_SZ)
]

# 目標: 修改 prev_ct 讓 plain 最後一個 byte 變成合法 padding
flag = b''
for block_idx in range(1, len(blocks)):

    prev_ct = blocks[block_idx - 1]
    cur_ct = blocks[block_idx]
    plain = b''

    # Target: guess == plain[-1]
    for pad in range(1, BLOCK_SZ+1):
        # pad: padding number, e.g., pad=3 -->  1 2 3 4 5 6 7 8 9 0 1 2 3 /x03 /x03 /x03 
        base = bytearray(prev_ct)
        for k in range(1, pad):
            base[-k] = prev_ct[-k] ^ plain[-k] ^ pad

        pos = BLOCK_SZ - pad
        for guess in range(256):
            # plain[pos] = Dec(plain)[pos] ^ prev_ct[pos]
            # if:   guess = plain[pos] 
            #   ->  guess = Dec(plain)[pos] ^ prev_ct[pos]
            #   ->  Dec(plain)[pos] = prev_ct[pos] ^ guess
            # target:
            #   Dec(plain)[pos] ^ IV_new[pos] = pad (合法 padding)
            #   ->  IV_new[pos] = prev_ct[pos] ^ guess ^ pad

            IV_new = base.copy()
            IV_new[pos] = prev_ct[pos] ^ guess ^ pad
            payload = IV_new + cur_ct

            if oracle(payload):
                if pad == 1:
                    check = IV_new.copy()
                    check[-2] ^= 1

                    if not oracle(check + cur_ct):
                        continue

                plain = bytes([guess])+ plain
                break
        if "}" in plain.decode():
            break
    flag += plain
    print(flag.decode())


print(f"flag = {flag}")