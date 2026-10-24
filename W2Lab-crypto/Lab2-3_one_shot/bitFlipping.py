from pwn import *


HOST = "45.77.20.255"
PORT = "31002"

r = remote(HOST, PORT)

r.recvuntil(b"Change the first block into ")

target_msg = r.recvline().strip()

ori_msg = bytes.fromhex(r.recvline().decode().split(':')[1])
cipher = bytes.fromhex(r.recvline().decode().split(':')[1])
 
r.recv() # One Shot >

#      iv_2 = cipher[1]  -> new cipher_1 = cipher[1] ^ (p_2 ^ target_msg)
fake_msg = xor(cipher[:16], ori_msg[16:32], target_msg) + cipher[16:32]

r.sendline(fake_msg.hex().encode())
print(r.recvall().decode())








