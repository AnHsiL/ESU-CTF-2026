from pwn import *
from sympy.ntheory import discrete_log
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256

p = 539886463685170284852407443970056803194248989742398797294074913090310265582980509535654551509645984788215337814031007413437004302678083874517375765338325720828816975723039
g = 2

HOST = "45.77.20.255" 
PORT = "31014"

r = remote(HOST, PORT)
p = int(r.recvline().strip().decode().split('=')[1])
g = int(r.recvline().strip().decode().split('=')[1])
pA = int(r.recvline().strip().decode().split('=')[1])
pB = int(r.recvline().strip().decode().split('=')[1])
enc = bytes.fromhex(r.recvline().strip().decode().split(' ')[1])
iv = bytes.fromhex(r.recvline().strip().decode().split(' ')[1])

a = discrete_log(p, pA, g)
key = sha256(str(pow(pB, a, p)).encode()).digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv)
print(unpad(cipher.decrypt(enc), 16))
