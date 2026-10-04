import os
import ast
from hashlib import sha256


def hash256(data):
    return sha256(data).digest()

def merge_nodes(a, b):
    return hash256(a+b)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(CUR_DIR, "output.txt")

flag = b''
with open (OUT_DIR, "r") as f:
    for line in f:
        line = line.strip()
        chal = ast.literal_eval(line)
        a = bytes.fromhex(chal[0])
        b = bytes.fromhex(chal[1])
        c = bytes.fromhex(chal[2])
        d = bytes.fromhex(chal[3])
        r = bytes.fromhex(chal[4])

        left = merge_nodes(a, b)
        right = merge_nodes(c, d)
        root = merge_nodes(left, right)

        flag = flag + b'1' if r == root else flag + b'0'

print(int(flag, 2).to_bytes((len(flag)+7)//8, 'big'))
