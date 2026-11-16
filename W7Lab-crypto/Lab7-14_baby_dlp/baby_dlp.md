#Crypto 

## 題目

**baby_dlp**

Something smooth ...

並附了 nc 和檔案，簡化後：
```python
def encrypt(key, msg):
    key = sha256(str(key).encode()).digest()[:16]
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(msg, 16)), iv

p = 53...9
g = 2
A = random.getrandbits(512)
pA = pow(g, A, p)
print(f"{p=}\n{g=}\n{pA=}")

B = random.getrandbits(512)
pB = pow(g, B, p)
print(f"{pB=}")
enc, IV = encrypt(pow(pB, A, p), flag2)
enc, IV = enc.hex(), IV.hex()
print(f"enc: {enc}\niv: {IV}")
```

## 解題
1. 觀察題目，很明顯是 DLP，smooth 可能指 (p-1) 的質因數 -> 用 [[Pollard’s p-1 Attack#Pollard’s p-1 Attack|Pollard’s p-1 Attack]] 
   > 用 `from sympy.ntheory import discrete_log` 工具

2. 用 `discrete_log()` 解出共同金鑰 $g^{AB}$
   ```python
   a = discrete_log(p, pA, g)
	key = sha256(str(pow(pB, a, p)).encode()).digest()[:16]
   ```
3. 解密
   ```python
   cipher = AES.new(key, AES.MODE_CBC, iv)
print(unpad(cipher.decrypt(enc), 16))
   ```
4. flag = `FLAG{afa8644153903d54946d02d2d5766a1b7ac89993cc8988e64a36e901fad37df5}`
   
