import subprocess
import hashlib
from pathlib import Path
from pwn import *

FASTCOLL_DIR = Path( r"\\wsl.localhost\Ubuntu-24.04\home\lahsi\ctf\fastcoll")
WSL_DIR = "/home/lahsi/ctf/fastcoll"

prefix = FASTCOLL_DIR / "prefix.bin"
msg1 = FASTCOLL_DIR / "msg1.bin"
msg2 = FASTCOLL_DIR / "msg2.bin"


HOST = "45.77.20.255"
PORT = "31012"
r = remote(HOST, PORT)

r.recvline() # U have 1 min, gogo!

for i in range(20):
    key = bytes.fromhex(r.recvline().decode())

    prefix.write_bytes(key)
    subprocess.run([
        "wsl",
        "-d", "Ubuntu-24.04",
        f"{WSL_DIR}/fastcoll",
        "-p", f"{WSL_DIR}/prefix.bin",
        "-o",
        f"{WSL_DIR}/msg1.bin",
        f"{WSL_DIR}/msg2.bin",
    ], check=True)

    m1 = msg1.read_bytes()
    m2 = msg2.read_bytes()

    r.recvuntil(b"1> ")
    r.sendline(m1.hex().encode())

    r.recvuntil(b"2> ")
    r.sendline(m2.hex().encode())

    r.recvline() # AC / WA

print(r.recvline())