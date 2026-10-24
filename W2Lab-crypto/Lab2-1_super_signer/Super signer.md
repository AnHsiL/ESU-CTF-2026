#Crypto

## 題目

**super_signer**
Welcome to my Super Signer System! I used AES ECB Mode to sign messages ... with my flag :)
`nc 45.77.20.255 31000`

並提供了 source code
```python
import os
from Crypto.Cipher import AES
from flags import flag2

# Initial datas
key=os.urandom(16)
aes=AES.new(key, AES.MODE_ECB)

def pad(data):
    return data+bytes([-len(data)%16]*(-len(data)%16))

if __name__=='__main__':
    print('=== Super Signer ===')
    while True:
        data=input('Input you message (hex) >')
        signed=aes.encrypt(pad(bytes.fromhex(data)+flag2))
        print(f"Signed:{signed.hex()}")
```

### Prepend Oracle Attack
利用 block encrypt 所需要的 padding 來攻擊演算法，並透過一個 "oracle" 反饋來得知訊息（訊息 == 解密成功與否）[^1][^2]
##### 攻擊條件
- 採用利用 Padding 的加密算法，並將很長的消息一塊一塊加解密
>非對稱加密中 OAEP 的填充方式也有可能會受到影響。
- 加密的分組模式爲 ECB
  ![[W2-1_ECB.png|581]]
##### 攻擊原理
![[W2-1_attack.png|603]]
假設長度為 `BLOCK_SIZE` ，送出 `BLOCK_SIZE` 長度的 payload 給 oracle，oracle 回復加密或經過操作的訊息
因為 ECB 是每個 block 分別加密的，可以透過送出 "長度 `BLOCK_SIZE - 1` 的 payload " 和 "長度 `BLOCK_SIZE - 1` 的 payload + 猜測字" ，後面訊息的第一個字會補到前一個 block 中，藉此用比對的方式暴力破解訊息
例如：`secret` = ILoveHoliday
- ECB 模式下的加密訊息
	```
	AAAAAAAAAAAAILoveHoliday
	```
- 可以送出 payload
  ```
  AAAAAAAAAAA
  ```
  和猜測字 a
  ```
  AAAAAAAAAAAa
  ```
- ECB 模式下的加密 payload 和 猜測句
  ```
  AAAAAAAAAAAI LoveHoliday
  AAAAAAAAAAAa ILoveHoliday
  ```

窮舉猜測字從 `a` 直到跟訊息第一個字 `I` 一樣
依序減少 payload 的數量直到結束
```
(加密訊息)：AILoveHolida y
(猜測字 a)：AILoveHolida a
```


## 解題
1. 連線後輸入隨機 hex 字串嘗試：
   ![[W2-1_nc.png]]
2. 觀察 source code：
   ```python
   signed=aes.encrypt(pad(bytes.fromhex(data)+flag2))
   ```
   可以看到加密的的內容是按照順序的 "輸入+flag" 
   --> 可利用 Prepend oracle attack
3. 設計腳本
   ```python
	from pwn import *
	
	HOST = "45.77.20.255"
	PORT = "31000"
	CHARSET = string.ascii_letters + string.digits + string.punctuation
	
	r = remote(HOST, PORT)
	
	def oracle(data):
	    r.recv() # Input you message (hex) >
	    r.sendline(data.encode().hex())
	    return r.recvline().decode().split(":")[1]
	
	print(r.recvline()) # === Super Signer ===
	
	BLOCK_SZ = 128
	flag = ""
	
	for i in range(1, BLOCK_SZ+1):
	    
	    flag_enc = oracle('A' *(BLOCK_SZ-i))
	    for c in CHARSET:
	        payload = ('A'*(BLOCK_SZ-i) + flag + c)
	        recv = oracle(payload)
	        if recv[:BLOCK_SZ*2] == flag_enc[:BLOCK_SZ*2]:
	            flag += c
	            print(flag)
	            break
	    if flag.endswith("}"):
	        break
	print(f"flag = {flag}")

   ```
   ![[W2-1_flag.png]]
4. flag = `FLAG{c10f733b5e646b0da92e51bcd31cc0604aab0f9ffa3baf44f571f49c8c7414c8}`

[^1]: [Padding Oracle Attack](https://hackmd.io/@starPt/B1gZo9-SB)
[^2]: [CTF wiki - Padding Oracle Attack](https://ctf-wiki.org/zh-tw/crypto/blockcipher/mode/padding-oracle-attack/)
