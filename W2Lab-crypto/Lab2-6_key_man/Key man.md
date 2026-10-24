#Crypto 

## 題目

**key_man**  

`nc 45.77.20.255 31005`

並提供了 source code，簡化後：

```python
IV = os.urandom(8)

def xor(a, b):
    return bytes(x ^ y for x,y in zip(a, b * (1 + len(a) // len(b))))

def encrypt(key, plaintext):
    try:
        plaintext = xor(plaintext, IV)
        
        cipher = DES3.new(key, DES3.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext)
        ciphertext = xor(ciphertext, IV)
        
        return ciphertext.hex()
    except:
        return 'Error'

print('You are the key man <3')
key = bytes.fromhex(input('> '))
print(encrypt(key, pad(flag, 8)))
print('Give u a gift')

while True:
    key = bytes.fromhex(input('(key)> '))
    plaintext = bytes.fromhex(input('(ctx)> '))
    print(encrypt(key, plaintext))

```

### DES weak key
DES 演算法共有 4個弱金鑰，會讓 16 回合產生的子金鑰完全相同，導致加密兩次會還原成明文[^2]。
- `0x0101010101010101`
- `0xfefefefefefefefe`
- `0xe0e0e0e0f1f1f1f1`
- `0x1f1f1f1f0e0e0e0e`
##### DES 子金鑰的生成步驟[^1]
64-bit 的初始金鑰 -> 產生 16 個 48-bit 子金鑰
1. **PC-1 置換**：剔除 8 個 priority bits，將剩餘的 56 bits 有效金鑰平分為左 $C_0$、右 $D_0$ 兩部分，各 28 bits
2. **循環左移**：每回合將 $C$ 和 $D$ 分別向左循環移位 1 或 2 bits
3. **PC-2 置換**：將每回合移位後的 $C_iD_i$（共 56 bits）透過壓縮置換轉為 48-bit 的子金鑰

| 原始 64 位元弱金鑰          | 經 PC-1 的 $C_0$         | 經 PC-1 的$D_0$          |
| -------------------- | ---------------------- | ---------------------- |
| `0x0101010101010101` | 全為 0 (`000...000`) | 全為 0 (`000...000`) |
| `0xFEFEFEFEFEFEFEFE` | 全為 1 (`111...111`) | 全為 1 (`111...111`) |
| `0xE0E0E0E0F1F1F1F1` | 全為 1 (`111...111`) | 全為 0 (`000...000`) |
| `0x1F1F1F1F0E0E0E0E` | 全為 0 (`000...000`) | 全為 1 (`111...111`) |
##### DES 類型弱金鑰攻擊方法
因為弱金鑰的特性，導致
$$
	\mathsf{DES}_k(\mathsf{DES}_k(M)) = M
$$
將密文用同一把金鑰重新加密可獲得明文
> [!abstract] 3-DES 上的弱金鑰攻擊
> 在 3-DES 上，使用 16-byte key，假設 key = `K1 | K2`，3-DES 內部會執行 
> ```
> E(K1) -> D(K2) -> E(K1)
> ```
> 若 `K1 = K2`，前兩步會互相抵消，退化成單一 DES
> --> 要使用弱金鑰在 3-DES 上，需選擇兩個不同的弱金鑰組合成一個

---

## 解題

1. 觀察 source code，發現：題目使用 DES3，並且輸入金鑰和密文後，會輸出加密結果
   -> 可自行決定金鑰 -> 可以使用 DES weak key 特性還原出 flag
2. 用同一把金鑰對加密後的 flag 重新加密
   ```python
	r = remote(HOST, PORT)
	
	r.recvuntil("> ")
	weak_key = "0101010101010101fefefefefefefefe" # 可替換成其他 3-DES 弱金鑰組合
	r.sendline(weak_key.encode())
	
	enc_flag = bytes.fromhex(r.recvline().decode().strip())
	
	r.recvline() # Give u a gift
	r.recvuntil("> ") # (key)> 
	r.sendline(weak_key.encode())
	
	r.recvuntil("> ") # (ctx)>
	r.sendline(enc_flag.hex().encode())
	
	flag = bytes.fromhex(r.recvline().decode().strip())
	print(flag)
   ```
1. flag = `FLAG{e181294a1b91175678019181bbdd7daa9c05c8d6b0ec3c056ff6f331fd5ece2c}`

[^1]: [Cryptography and Network Security-ch6](https://assam1231.blogspot.com/2015/01/cryptography-and-network-security-ch6.html)
[^2]: [求解 DES 弱密钥](https://csmantle.top/2025/11/16/finding-weak-keys-in-des.html)
