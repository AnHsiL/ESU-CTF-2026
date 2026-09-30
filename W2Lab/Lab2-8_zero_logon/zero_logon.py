from pwn import *
import os

HOST = "45.77.20.255"
PORT = "31007"

r = remote(HOST, PORT)
SUCCEED = "Welcome"

while True:
    r.recvuntil("Challenge: ")

    fake_pw = b'\x00' *32
    r.sendline(fake_pw.hex().encode())

    r.recvuntil("Token: ")
    token = b'\x00' * 16
    r.sendline(token.hex().encode())

    if SUCCEED in r.recvline().decode():
        print(r.recvline().decode())
        break
