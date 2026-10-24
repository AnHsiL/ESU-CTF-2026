#Crypto 

## 題目

**babyaes**  
This was an old challenge I made for the 1st THJCC! ~~Not so baby actually :)))))))~~

`nc 45.77.20.255 310078`

並提供了 source code，簡化後：

```python
ecb = AES.new(key, AES.MODE_ECB)
cbc = AES.new(key, AES.MODE_CBC, IV)
passphrase=b'eating_whale...'

def pad(data):
    p = (-len(data) % 16)
    return data + bytes([p]) * p

def chk_pad(data):
    if len(data)==16:
        print("Padding Correct")
    elif not all([x == data[-1] for x in data[-data[-1]:]]):
        print("Padding Error")
    else:
        print("Padding Correct")

def sign(x):
    x=pad(x)
    return hmac.new(key, x, 'sha256').hexdigest()

def MBC(x):
    x=pad(x)
    iv=IV
    final=b''
    for i in range(0, len(x), 16):
        cur=ecb.encrypt(x[i:i+16])
        final+=xor(iv, cur)
        iv=x[i:i+16]
    return final

isadmin=False
while isadmin==False:
    print("1.Verify your identity:")
    print("2.Sign a message")
    option=int(input("Option(1/2):"))
    if option==1:
        x=input("Your signed key(hex encoded):")
        if sign(passphrase)==x:
            print("Verified!!!")
            isadmin=True
        else:
            print("Failed")
    else:
        x=input("Sign a message(hex encoded):")
        if bytes.fromhex(x)==passphrase:
            print("Bad Hacker :(")
        else:
            print(sign(bytes.fromhex(x)))

print("This is the encrypted flag(CBC MODE): ")
print(cbc.encrypt(pad(flag)).hex())
cbc = AES.new(key, AES.MODE_CBC, IV)
while True:
    print("Option 1: MBC MODE Encrypter")
    print("Option 2: CBC MODE Pad Checker")
    option=int(input("Your option(1/2):"))
    if option == 1:
        x=input("Encrypt a message(hex encoded):")
        print(MBC(bytes.fromhex(x)).hex())
    elif option == 2:
        x=input("Check a padding(hex encoded):")
        chk_pad(cbc.decrypt(pad(bytes.fromhex(x))))
    else:
        print("Invalid method...")
```


---

## 解題

1. 觀察 source code，發現：
   - 題目有兩關
	   1. 成為 admin 並獲取加密後的 flag
	   2. 有 oracle 存在 ->利用 oracle 解密 flag
   - 獲取 admin 權限的判斷中不允許與 `passphrase` 一樣
     ```python
     x=input("Sign a message(hex encoded):")
	if bytes.fromhex(x)==passphrase:
			print("Bad Hacker :(")
	else:
			print(sign(bytes.fromhex(x)))
     ```
     但 `passphrase` 的長度不是 16 -> 可以自行完善 padding 達成「與 signed `passphrase` 不同」但「值相同」的特性
   - flag 的加密方法是 CBC，每個 block 的加密有相依性 -> 可以 xor 還原特定的值
   - 存在 padding oracle `chk_pad()` 回答 padding 是否符合規定
1. 成為 admin：
   `passphrase` 是 15 個字，先使 padding 符合送出進行 sign，把 signed key 送出後獲取 admin 權限和 `enc_flag`，簡化程式碼：
   ```python
	r = remote(HOST, PORT)
	passphrase=b'eating_whale...'
	
	r.recv() # Sign a message(hex encoded):
	msg = pad(passphrase)
	r.sendline(msg.hex().encode())
	signed_msg = r.recv().decode().strip()
	
	r.recv() # Your signed key(hex encoded):
	r.sendline(signed_msg.encode())
	
	enc_flag = r.recvline().decode().strip()
   ```
2. 送出加密 2 $\times$ 16 個 `'A'` ，用 CBC 特性把 c1、c2、明文 xor 起來獲取 IV，簡化程式碼：
   ```python
   block = b"A" * 16
   
	r.recvuntil("Encrypt a message(hex encoded):")
	r.sendline((block * 2).hex().encode())
	
	mbc = bytes.fromhex(r.recvline().decode().strip())
	B1 = mbc[:16]
	B2 = mbc[16:32]
	
	IV = xor(B1, B2, block)
	print(f"IV: {IV}")
   ```
3. 用 Padding oracle attack 破解，簡化版
   ```python
   def oracle(data):
	    r.recvuntil("Check a padding(hex encoded):")
	    r.sendline(data.hex().encode())
	    return "Padding Correct" in r.recvline().decode()
	
	BLOCK_SZ = 16
	
	cipher = bytes.fromhex(enc_flag)
	blocks = [ cipher[i:i+16] for i in range(0, len(cipher), 16)]
	
	flag = b''
	for block_idx in range(0, len(blocks)):
	    prev_ct = IV if block_idx == 0 else blocks[block_idx - 1]
	    cur_ct = blocks[block_idx]
	    plain = b''
	
	    for pad in range(1, BLOCK_SZ+1):
	        base = bytearray(prev_ct)
	        for k in range(1, pad):
	            base[-k] = prev_ct[-k] ^ plain[-k] ^ pad
	
	        pos = BLOCK_SZ - pad
	        for guess in range(256):
	            IV_new = base.copy()
	            IV_new[pos] = prev_ct[pos] ^ guess ^ pad
	            payload = IV_new + cur_ct
	
	            if oracle(payload):
	                plain = bytes([guess])+ plain
	                break
	                
	    flag += plain
	    print(flag.decode())

   ```
4. flag = `FLAG{bcfebf591fd01d377eb9f976e19e2ded6ae1dba5bb4f7ff25d3f0ac4f78}`
