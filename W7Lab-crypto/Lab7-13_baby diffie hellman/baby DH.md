#Crypto 

## 題目
**baby_diffie_hellman**

Your first Diffie-Hellman.
並給了 nc 連線 和 source code

簡化後：
```python
def encrypt(key, msg):
    key = sha256(str(key).encode()).digest()[:16]
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(msg, 16)), iv

p = getPrime(512)
g = 2
A = random.getrandbits(512)
pA = pow(g, A, p)
print(f"{p=}\n{g=}\n{pA=}")

pB = int(input("pB: "))
enc, IV = encrypt(pow(pB, A, p), flag1)
enc, IV = enc.hex(), IV.hex()
print(f"enc: {enc}\niv: {IV}")
```

## 解題
![[W7-14_nc.png]]
1. 題目提供 `p`、`g`、`pA`，我們可以控制 `pB` 的輸入，題目回傳 `enc`和`iv`
2. 觀察 source code 
   ```python
   enc, IV = encrypt(pow(pB, A, p), flag1)
   ```
   -> 可以控制 `pB` = 1 使加密用 1 為密鑰
3. 解題
   ```python
	
	def decrypt(key, enc, iv):
	    key = sha256(str(key).encode()).digest()[:16]
	    cipher = AES.new(key, AES.MODE_CBC, iv)
	    return unpad(cipher.decrypt(enc), 16)
	
	HOST = "45.77.20.255" 
	PORT = "31013"
	
	r = remote(HOST, PORT)
	p = r.recvline().decode().split('=')[1]
	g = r.recvline().decode().split('=')[1]
	pA = r.recvline().decode().split('=')[1]
	pB = 1  # pow(1, A, p) = 1
	
	r.sendlineafter(b"pB: ", str(pB).encode())
	enc = bytes.fromhex(r.recvline().decode().split(': ')[1])
	iv = bytes.fromhex(r.recvline().decode().split(': ')[1])
	
	print(decrypt(pB, enc, iv))
   ```

4. flag = `FLAG{aee2f708f057adac32a43c7c6b8a80b4bc5d41384cf272810437303bb7e12100}`