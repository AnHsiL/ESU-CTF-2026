#Crypto 

## 題目

**Padding Oracle Attack**  
psychic_msg  
`nc 45.77.20.255 31003`

並提供了 source code，簡化後：

```python
def encrypt(IV, data):
    aes = AES.new(key, AES.MODE_CBC, IV)
    return aes.encrypt(data)

def decrypt(IV, data):
    aes = AES.new(key, AES.MODE_CBC, IV)
    return aes.decrypt(data)

if __name__ == '__main__':
    print(
        f"Encrypted Flag:"
        f"{cur_iv.hex() + encrypt(cur_iv, pad(flag4)).hex()}"
    )

    while True:
        msg = input("Your Message (hex) >")
        msg = bytes.fromhex(msg)

        try:
            unpad(decrypt(msg[:16], msg[16:]))
            print('I got that message!')
        except ValueError:
            print('What were you talking about?')
```

### Padding Oracle Attack
Padding Oracle Attack 常出現在 **CBC Mode + PKCS#7 Padding** 的情況
**限制**：需要 Oracle 提供 Padding 是否正確的資訊，逐 byte 猜出 plaintext。

##### PKCS#7 合法 Padding：
```text
pad = 1 -> 01
pad = 2 -> 02 02
pad = 3 -> 03 03 03
...
pad = 16 -> 10 10 10 ... 10
```

##### CBC 解密
例如要破解 `P2`：

```text
                  C2
                  ▼
            ┌───────────┐
            │ AES 解密  │
            └───────────┘
                  ▼
               Dec(C2)
                  ▼
C1 ────────────> XOR
                  ▼
                  P2
```

只要修改前面的 `C1`，就可以控制最後產生的 `P2`。

#### 攻擊手法
從明文最後一個 byte 開始猜
```text
P2 = ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??
```
- 目標：修改 `C1`，讓 Server 解出的最後一個 byte 變成 `01`，也就是合法的 1-byte Padding：
	```text
	P2 = ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 01
	```
- 希望： `guess` = 原本的 `P2[pos]`

##### 推演
```python
plain[pos] = Dec(plain)[pos] ^ C1[pos]

if:   guess = plain[pos]
   ->  guess = Dec(plain)[pos] ^ C1[pos]
   ->  Dec(plain)[pos] = C1[pos] ^ guess
target:
   Dec(plain)[pos] ^ C1_new[pos] = pad (合法 padding)
   ->  C1_new[pos] = C1[pos] ^ guess ^ pad
```
##### 整體破解流程：

```text
+ pad = 1
	???????????????? 
	               ↑
	            guess
	成功：
	???????????????A
	▼
+ pad = 2
	??????????????BA
	              ↑
	pad 修改成：
	??????????????02 02
	▼
+ pad = 3
	?????????????ABC
				 ↑
	pad 修改成：
	?????????????03 03 03
```

直到整個 16-byte Block 破解完成

---

## 解題

1. 觀察 source code，發現：
   - 使用 `MODE_CBC`
   - Server 將 `IV + Ciphertext` 一起輸出
     ```
     Encrypted Flag: 
     [ IV ][ C1 ][ C2 ][ C3 ] ...
     ```
   - Padding 正確與錯誤會產生不同訊息 -> Server 本身就是一個 **Padding Oracle**。

1. CBC 解密：每次取相鄰的兩個 block `prev_ct | cur_ct`，修改 `prev_ct`，利用 Oracle 判斷破解：
   ```
   cur_ct
      ▼
   Dec(cur_ct)
      │
      XOR
      │
   modified prev_ct
      ▼
   plaintext
      ▼
   Padding 是否正確？
   ```
2. 整體流程
   ```
	Encrypted Flag
	[ IV ][ C1 ][ C2 ][ C3 ] ...
	   └─────┴──────> 破解 P1
	
	        [ C1 ][ C2 ]
	           └─────┴──> 破解 P2
	
	               [ C2 ][ C3 ]
	                  └─────┴──> 破解 P3
   ```
   每一個 block 裡再從最後一個 byte 往前：
	```text
	????????????????
	               ↑ pad = 1
	
	???????????????A
	              ↑  pad = 2
	
	??????????????BA
	             ↑   pad = 3
	...
	```


3. 寫腳本
   ```python
	r = remote(HOST, PORT)
	
	r.recvuntil("Encrypted Flag:")
	enc_flag = bytes.fromhex(r.recvline().decode().strip())
	
	def oracle(data):
	    r.recvuntil(b"Your Message (hex) >") # Your Message (hex) >
	    r.sendline(data.hex().encode())
	    
	    res = r.recvline().decode()
	    return "I got that message!" in res
	
	BLOCK_SZ = 16
	blocks = [
	    enc_flag[i:i + BLOCK_SZ] for i in range(0, len(enc_flag), BLOCK_SZ)
	]
	
	# 目標: 修改 prev_ct 讓 plain 最後一個 byte 變成合法 padding
	flag = b''
	for block_idx in range(1, len(blocks)):
	
	    prev_ct = blocks[block_idx - 1]
	    cur_ct = blocks[block_idx]
	    plain = b''
	
	    # Target: guess == plain[-1]
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
	                if pad == 1:
	                    check = IV_new.copy()
	                    check[-2] ^= 1
	                    if not oracle(check + cur_ct):
	                        continue
	
	                plain = bytes([guess])+ plain
	                break
	    flag += plain
	    print(flag.decode())
	
	print(f"flag = {flag}")
   ```
   ![[W2-4_flag.png|center]]
3. flag = `FLAG{e9c862645d767463862be7f428abd5d6b3204cecdea3808bfac8d6e73fe68938}`