from pwn import *
from hashlib import md5
import HashTools

HOST = "45.77.20.255"
PORT = "31010"
r = remote(HOST, PORT)

target = b'meet me next wednesday'
payload = b'A' *16

r.sendlineafter(b"CMD > ", b"SIGN")
r.sendlineafter(b"MSG > ", payload.hex().encode())

rec_sign = r.recvline().decode().strip()

# MD5 Length Extension Attack
new_MD5 = HashTools.new("md5")
msg, sign = new_MD5.extension(
    secret_length=16,       # salt 長度
    original_data=payload,
    append_data=target,
    signature=rec_sign
)

r.sendlineafter(b"CMD > ", b"SEND")
r.sendlineafter(b"MSG > ", msg.hex().encode())

r.sendlineafter(b"SIG > ", sign.encode())
r.recvline()  # GOOD, I've READ IT
print(r.recvline().decode())
