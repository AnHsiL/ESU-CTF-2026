from pwn import *

def pad(data):
    p = (-len(data) % 16)
    return data + bytes([p]) * p


HOST = "45.77.20.255"
PORT = "31008"

r = remote(HOST, PORT)

# ----------------------------
#
# to admin
#
# ----------------------------

passphrase=b'eating_whale...'

r.recvuntil("Option(1/2):")
r.sendline(b'\x02'.hex().encode())
r.recv() # Sign a message(hex encoded):

msg = pad(passphrase)
r.sendline(msg.hex().encode())
signed_msg = r.recv().decode().strip()

r.recvuntil("Option(1/2):")
r.sendline(b'\x01'.hex().encode())
r.recv() # Your signed key(hex encoded):
r.sendline(signed_msg.encode())
r.recvuntil("This is the encrypted flag(CBC MODE): \n")
enc_flag = r.recvline().decode().strip()

# ----------------------------
#
# get IV
#
# ----------------------------
block = b"A" * 16

r.recvuntil("Your option(1/2):")
r.sendline(b'\x01'.hex().encode())

r.recvuntil("Encrypt a message(hex encoded):")
r.sendline((block * 2).hex().encode())
mbc = bytes.fromhex(r.recvline().decode().strip())

B1 = mbc[:16]
B2 = mbc[16:32]

IV = xor(B1, B2, block)
print(f"IV: {IV}")

# ----------------------------
#
# Padding oracle attack
#
# ----------------------------

def oracle(data):
    r.recvuntil("Your option(1/2):")
    r.sendline(b'\x02'.hex().encode())
    r.recvuntil("Check a padding(hex encoded):")
    r.sendline(data.hex().encode())
    return "Padding Correct" in r.recvline().decode()

BLOCK_SZ = 16

cipher = bytes.fromhex(enc_flag)
blocks = [ cipher[i:i+16] for i in range(0, len(cipher), 16)]

flag = b''
for block_idx in range(0, len(blocks)):
    prev_ct = IV if block_idx == 0 else blocks[block_idx - 1]
    cur_ct = blocks[block_idx]
    plain = b''

    for pad in range(1, BLOCK_SZ+1):
        base = bytearray(prev_ct)
        for k in range(1, pad):
            base[-k] = prev_ct[-k] ^ plain[-k] ^ pad

        pos = BLOCK_SZ - pad
        for guess in range(256):
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

