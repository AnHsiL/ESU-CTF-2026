#Crypto 

## 題目

**daes**  
Yeah, I do AES twice, double secured!

`nc 45.77.20.255 31006`

並提供了 source code，簡化後：

```python
signal.alarm(TIMEOUT)

target = os.urandom(16)

keys = [b'whalekey:' + str(random.randrange(1000000, 1999999)).encode() for _ in range(2)]

def enc(key, msg):
    ecb = AES.new(key, AES.MODE_ECB)
    return ecb.encrypt(msg)

def daes(msg):
    tmp = enc(keys[0], msg)
    return enc(keys[1], tmp)

test = b'you are my fire~'
print(daes(test).hex())
print(daes(target).hex())

ans = input("Ans:")

if ans == target.hex():
    print(flag)
```

### MitM Attack in Double DES
Meet-in-the-Middle（MitM） Attack 主要攻擊 double DES，用以降低暴力破解的時間
- Double DES 流程：
```
				    k0           k1
					▼            ▼
				┌───────┐ tmp ┌───────┐
	plaintext -> │  Enc  │ --> │  Enc  │ -> ciphertext
				└───────┘     └───────┘
```
假設 Double DES 是 `C = E(K2, E(K1, P))`，MitM：
```
從明文往前算：
tmp0 = Enc(k0, P)

從密文往後算：
tmp1 = Dec(k1, C)
```
可以從 `tmp0 == tmp1 == tmp` 推出 `k0`、`k1` 的值


---

## 解題

1. 觀察 source code，發現：
   - 題目有 timeout 限制，暴力破解不行
   - key 個產生方式是 "whalekey:" + 1000000 ~1999999 間的隨機數值
   - 題目提供 `enc()` 和 `dec()`，並且給了 `test` 的明文-密文 對
   - **目標**：得到 Double DES keys 並解密題目提供的 `enc(target)`
1. 用 MitM attack：
	1. 建立 "可能的 k0" 對應表
	   ```python	   
	   for i in KEY_RANGE:
		   val = enc(i, test)
		   tmp0[val] = i
	   ```
	2. 建立 "可能的 k1" 陣列同時，比對 k0 的對應表中是否出現共同的值（Double DES 中的 tmp）
	   ```python	   
	   for i in KEY_RANGE:		    
		   val = dec(i , enc_test)
		   if val in tmp0:
			   k1 = i
			   k0 = tmp0[val]
			   break
	   ```
2. 寫腳本
   ```python
	r = remote(HOST, PORT)
	
	test = b'you are my fire~'
	enc_test = bytes.fromhex(r.recvline().decode().strip())
	enc_target = bytes.fromhex(r.recvline().decode().strip())
	
	def enc(key, msg):
	    ecb = AES.new(key, AES.MODE_ECB)
	    return ecb.encrypt(msg)
	
	def dec(key, cipher):
	    ecb = AES.new(key, AES.MODE_ECB)
	    return ecb.decrypt(cipher)
	
	def toKey(key):
	    return b'whalekey:'+str(key).encode()
	
	# Build table
	KEY_RANGE = range(1000000, 1999999)
	tmp0 = {}
	for i in KEY_RANGE:
	    val = enc(toKey(i), test)
	    tmp0[val] = i
	
	# find common value
	k0 = -1
	k1 = -1
	for i in KEY_RANGE:
	    val = dec(toKey(i) , enc_test)
	    if val in tmp0:
	        k1 = toKey(i)
	        k0 = toKey(tmp0[val])
	        break
	
	r.recvuntil(":") # Ans:
	
	# decrypt target
	target = dec(k0, dec(k1, enc_target))
	r.sendline(target.hex().encode())
	print(r.recv().decode())
   ```
1. flag = `FLAG{2733ccc0b3f8d33a67459d038526361f33ef6e75fa36ec6d3d16354b0a8bc18d}`

