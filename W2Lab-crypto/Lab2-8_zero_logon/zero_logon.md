#Crypto 

## 題目

**zero_logon**  
The Great Zero Logon vulnerability! Was patched by MicroSoft, but probably not MeowcroSoft.

`nc 45.77.20.255 31007`

並提供了 source code，簡化後：

```python
class CFB8:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        IV = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_ECB)
        ct = b''
        state = IV
        for i in range(len(plaintext)):
            b = cipher.encrypt(state)[0]
            c = b ^ plaintext[i]
            ct += bytes([c])
            state = state[1:] + bytes([c])
        return IV + ct

    def decrypt(self, ciphertext):
        IV = ciphertext[:16]
        ct = ciphertext[16:]
        cipher = AES.new(self.key, AES.MODE_ECB)
        pt = b''
        state = IV
        for i in range(len(ct)):
            b = cipher.encrypt(state)[0]
            c = b ^ ct[i]
            pt += bytes([c])
            state = state[1:] + bytes([ct[i]])
        return pt

print("Welcome to the MeowcroSoft login portal 🐾")
admin_password = os.urandom(16)

while True:
    cur_time = str(time())
    print(f"Current TimeStamp: {cur_time}")
    client_challenge = bytes.fromhex(input("Challenge: "))
    if len(client_challenge) != 32:
        print("Error: incorrect client challenge length")
        continue
    
    cipher = CFB8(md5(cur_time.encode() + admin_password).digest())
    client_token = cipher.decrypt(client_challenge)
    input_token = bytes.fromhex(input("Token: "))
    if client_token == input_token:
        print(f"Welcome, admin\n{flag}")
    else:
        print("Login Failed QwQ")

```

### ZeroLogon
**ZeroLogon**（CVE-2020-1472）：Netlogon 在認證時錯誤使用 AES-CFB8 + 全 0 IV，導致攻擊者只要一直送全 0 的 challenge / credential，就有 1/256 的機率被當成合法[^1]
![[W2-7_ZeroLogon.png|677]]
為什麼是 1/256 的機率？
> AES-CFB8 中，當輸入也全是 `0` 時，如果 AES 算出的第一個 byte 剛好也是 `00`，後面的狀態就會持續維持全 `0`，使 ciphertext 為全 `0`
> 一個 byte 有 `00` ~ `FF` 256 種可能 -> 碰到 `00` 的機率約為 1/256

##### 攻擊流程
攻擊者送全 `0` Challenge + 全 `0` ciphertext --(不停重試)--> 約 1/256 機率認證成功


---

## 解題

1. 觀察 source code，發現：
   - 題目是 zero_logon -> 利用 zero logon 漏洞
   - 使用 `CFB8` 加密，密文的前 16 bytes 是加密的訊息、後 16 bytes 是 IV
   - **目標**：繞過加解密驗證獲得 flag
2. 寫腳本
   ```python
	r = remote(HOST, PORT)
	SUCCEED = "Welcome"
	
	while True:
	    r.recvuntil("Challenge: ")
	
	    fake_pw = b'\x00' *32  # ciphertext(16) + IV(16)
	    r.sendline(fake_pw.hex().encode())
	
	    r.recvuntil("Token: ")
	    token = b'\x00' * 16   # 跟 ciphertext 長度一致
	    r.sendline(token.hex().encode())
	
	    if SUCCEED in r.recvline().decode():
	        print(r.recvline().decode())
	        break
   ```
3. flag = `FLAG{de09fb671b07ca861715214d19304b61bc158109abc103c6795e0691698fc4a1}`

[^1]: [何謂Zerologon？ | 趨勢科技(TW)](https://www.trendmicro.com/zh_tw/what-is/zerologon.html)
