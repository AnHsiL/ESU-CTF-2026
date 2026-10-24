#Crypto 

## 題目

**broken_menu**  

`nc 45.77.20.255 31004`

並提供了 source code，簡化後：

```python
key = os.urandom(32)
nonce = os.urandom(12)

def encrypt(message):
   cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
   ciphertext, tag = cipher.encrypt_and_digest(message)
   return ciphertext + tag + nonce

def decrypt(message_enc):
   ciphertext = message_enc[:-28]
   tag = message_enc[-28:-12]
   nonce = message_enc[-12:]
   cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
   plaintext = cipher.decrypt_and_verify(ciphertext, tag)
   return plaintext

menu = [b"Mixtured curry with rice - 120 TWD", 
	b"\"Automated\" Cafe Mocha - 45 TWD",
	b"Secret FLAG :>"]

for i in range(2):
    print('> ', encrypt(menu[i]).hex())

patch = input('> ')
if menu[2] in decrypt(bytes.fromhex(patch)):
    print(flag)
else:
    print('=' * 24, 'Recovery Failed :<', '=' * 24)

```

### Poly1305
一種 MAC（Message Authentication Code），用以驗證完整性，確認訊息是否被修改且是否由對方產生
Poly1305 會把加密訊息切成多個 block，在 $mod (2^{130} - 5)$ 做類似多項式運算
- `r`：多項式運算的 key
- `s`：最後加上的遮罩值
```python
H1 = m1 * r
H2 = (H1 + m2) * r
...

--> H = (((m1 * r + m2) * r + m3) * r + ...)
--> tag = (H + s) mod 2^128
```

接收端在解密密文後，重新生成 tag 比對

---

## 解題

1. 觀察 source code，發現：
   - 密文組成：
     ```
     ciphertext + tag + nonce 
				    28 + 12 bytes
     ```
 - 目標：偽造出 `menu[2]` = `b"Secret FLAG :>"` 的密文並通過 poly1305 完整性驗證

1. 寫 `ploy1305` 的腳本
   > ~~這邊我不會，請 GPT 代勞了~~ ╮(￣▽￣)╭

	產出
	- `p_coeff(ct)`：建立 ChaCha20-Poly1305 實際拿去 MAC 的多項式
	- `p_eval`：產生 MAC（[[#Poly1305]] 的 `H()`）
	- `recover_rs`：從兩對（明文, 密文）推出多項式運算的 key `r` 和遮罩 `s`
2. 寫腳本（簡化）
   ```python
	c0 = rec0[:-28]
	c1 = rec1[:-28]
	
	# KS = P1 XOR C0 -> C3 = P3 XOR KS
	keyStream = xor(msg[0],c0) 
	c2 = xor(msg[2], keyStream[:len(msg[2])])
	
	from poly1305 import recover_rs, p_eval, p_coeff, MOD128
	
	nonce = rec0[-12:]
	tag0 = rec0[-28:-12]
	tag1 = rec1[-28:-12]
	
	rd, s = recover_rs( c0, tag0, c1, tag1)
	
	# Tag = message * rd + s
	tag2 = (p_eval(p_coeff(c2), rd) + s) % MOD128
	tag2 = tag2.to_bytes(16, "little")
	
	fake_cipher = c2 + tag2 + nonce
	
	r.sendline(fake_cipher.hex().encode())
	print(r.recv().decode())
   ```
   ![[W2-5_flag.png|597]]
2. flag = `FLAG{0dec5da583613789cb06730e9452d8c9011ac945b6e1bda0b7673361683c8d15}`