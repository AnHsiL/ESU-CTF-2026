import hashlib
import json
import os
from Crypto.Cipher import AES


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CUR_DIR, "data.json")

with open(DATA_DIR, "r") as f:
    data = json.load(f)
    iv = bytes.fromhex(data["iv"])
    enc = bytes.fromhex(data["enc"])
    public_key = [bytes.fromhex(x) for x in data["public_key"]]

    hashes = []
    signatures = []
    for record in data["signatures"]:
        message = record["message"].encode()
        hashes.append(hashlib.sha256(message).digest())

        signature = [bytes.fromhex(x) for x in record["signature"]]
        signatures.append(signature)

target_msg = (f"{public_key[0].hex()} sent 999999 WOTScoins to me").encode()
target_hash = hashlib.sha256(target_msg).digest()
target_signature = []

for i in range(32):
    target = target_hash[i]

    for j in range(len(hashes)):
        known = hashes[j][i]

        if known >= target:
            sig = signatures[j][i]

            for _ in range(known - target):
                sig = hashlib.sha256(sig).digest()

            target_signature.append(sig)
            break

aes_key = bytes([s[0] for s in target_signature])
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
flag = cipher.decrypt(enc)

print(flag)