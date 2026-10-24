from pwn import *

HOST = "45.77.20.255"
PORT = "31001"

r = remote(HOST, PORT)
r.recvline() # === Welcom to Trillion Bank ===

def chooseOption(choice):
    r.recvlines(3)
    r.recv() # Your option (1/2):
    r.sendline(str(choice).encode())
    r.recv() # Your name:


PAD_LEN = 16

chooseOption(1)

# 'user:'+name+';amount:10'
payload = 'A'*(PAD_LEN-len('user:'))+';amount:'+'9'*(PAD_LEN-len(';amount:'))+'9'*(PAD_LEN)

# session 取 len(f'user:{payload}') // PAD_LEN = 3 個 blocks
#       = 48 個 bytes = 十六進制 2 字母一個 byte -> 前 48*2 = 96 個字母

r.sendline(payload.encode())
session = r.recvline().decode()[:96]

chooseOption(2)
r.sendline(session.encode())

print(r.recv().decode().split('\n')[1])
