from pwn import *


HOST = "45.77.20.255"
PORT = "31005"

r = remote(HOST, PORT)

r.recvuntil("> ")

weak_key = "0101010101010101fefefefefefefefe"
r.sendline(weak_key.encode())

enc_flag = bytes.fromhex(r.recvline().decode().strip())

r.recvline() # Give u a gift
r.recvuntil("> ") # (key)> 
r.sendline(weak_key.encode())

r.recvuntil("> ") # (ctx)>
r.sendline(enc_flag.hex().encode())

flag = bytes.fromhex(r.recvline().decode().strip())
print(flag)