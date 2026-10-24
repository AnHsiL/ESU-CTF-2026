# Prepend Oracle Attack
from pwn import *

HOST = "45.77.20.255"
PORT = "31000"
CHARSET = string.ascii_letters + string.digits + string.punctuation

r = remote(HOST, PORT)


def oracle(data):

    r.recv() # Input you message (hex) >
    r.sendline(data.encode().hex())

    return r.recvline().decode().split(":")[1]



print(r.recvline()) # === Super Signer ===

BLOCK_SZ = 128
flag = ""

for i in range(1, BLOCK_SZ+1):
    
    flag_enc = oracle('A' *(BLOCK_SZ-i))
    for c in CHARSET:
        payload = ('A'*(BLOCK_SZ-i) + flag + c)
        recv = oracle(payload)
        if recv[:BLOCK_SZ*2] == flag_enc[:BLOCK_SZ*2]:
            flag += c
            print(flag)
            break
    if flag.endswith("}"):
        break
print(f"flag = {flag}")
