from pwn import *
from Crypto.Cipher import AES


HOST = "45.77.20.255"
PORT = "31006"

r = remote(HOST, PORT)

test = b'you are my fire~'
enc_test = bytes.fromhex(r.recvline().decode().strip())
enc_target = bytes.fromhex(r.recvline().decode().strip())

def enc(key, msg):
    ecb = AES.new(key, AES.MODE_ECB)
    return ecb.encrypt(msg)

def dec(key, cipher):
    ecb = AES.new(key, AES.MODE_ECB)
    return ecb.decrypt(cipher)

def toKey(key):
    return b'whalekey:'+str(key).encode()

# Build table
KEY_RANGE = range(1000000, 1999999)
tmp0 = {}
for i in KEY_RANGE:
    val = enc(toKey(i), test)
    tmp0[val] = i

# find common value
k0 = -1
k1 = -1
for i in KEY_RANGE:
    val = dec(toKey(i) , enc_test)
    if val in tmp0:
        k1 = toKey(i)
        k0 = toKey(tmp0[val])
        break


r.recvuntil(":") # Ans:

# decrypt target
target = dec(k0, dec(k1, enc_target))
r.sendline(target.hex().encode())
print(r.recv().decode())