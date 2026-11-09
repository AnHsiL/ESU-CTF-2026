from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256


def decrypt(key, enc, iv):
    key = sha256(str(key).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc), 16)

HOST = "45.77.20.255" 
PORT = "31013"

r = remote(HOST, PORT)
p = r.recvline().decode().split('=')[1]
g = r.recvline().decode().split('=')[1]
pA = r.recvline().decode().split('=')[1]
pB = 1  # pow(1, A, p) = 1

r.sendlineafter(b"pB: ", str(pB).encode())
enc = bytes.fromhex(r.recvline().decode().split(': ')[1])
iv = bytes.fromhex(r.recvline().decode().split(': ')[1])

print(decrypt(pB, enc, iv))