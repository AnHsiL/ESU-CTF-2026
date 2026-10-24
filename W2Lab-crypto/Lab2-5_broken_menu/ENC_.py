from pwn import *

msg = [b"Mixtured curry with rice - 120 TWD", 
b"\"Automated\" Cafe Mocha - 45 TWD",
b"Secret FLAG :>"]

HOST = "45.77.20.255"
PORT = "31004"

r = remote(HOST, PORT)

r.recvuntil(b">  ")
rec0 = bytes.fromhex(r.recvline().decode().strip())
r.recvuntil(b">  ")
rec1 = bytes.fromhex(r.recvline().decode().strip())
r.recvline() # ===  3RR: menu broken  ===
r.recv()

c0 = rec0[:-28]
c1 = rec1[:-28]

# KS = P1 XOR C0 -> C3 = P3 XOR KS
keyStream = xor(msg[0],c0) 
c2 = xor(msg[2], keyStream[:len(msg[2])])


from poly1305 import recover_rs, p_eval, p_coeff, MOD128

nonce = rec0[-12:]
tag0 = rec0[-28:-12]
tag1 = rec1[-28:-12]

rd, s = recover_rs( c0, tag0, c1, tag1)

# Tag = message * rd + s
tag2 = (p_eval(p_coeff(c2), rd) + s) % MOD128
tag2 = tag2.to_bytes(16, "little")

fake_cipher = c2 + tag2 + nonce

r.sendline(fake_cipher.hex().encode())
print(r.recv().decode())