#Crypto 

## 題目

**Bit-flipping attack**
One Shot and make some advertisement for me uwub
`nc 45.77.20.255 31002`

並提供了 source code，簡化後：
```python
def encrypt(data):
    aes=AES.new(key, AES.MODE_CBC, iv)
    return aes.encrypt(data)

def decrypt(data):
    aes=AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(data)

# Main Function
if __name__=='__main__':
    chal=os.urandom(32)
    print(f'Original Message:{chal.hex()}')
    print(f'Encrypted:{encrypt(chal).hex()}')
    shot=input('One Shot >')
    result=decrypt(bytes.fromhex(shot))
    if b'wha13.github.io/' in result:
        print(flag3)
    else:
        print('Failed...')
```


### Bit-flipping attack
透過修改密文，在不需知道金鑰或完整明文的情況下，達到操縱解密結果的攻擊手法

常見於如 CBC 模式 或 CTR 模式 等區塊加密模式，攻擊者透過攔截修改密文（或初始向量 IV），利用 XOR 的特性，使解密後的明文變成攻擊者預期且可控制的內容。

##### Cipher-block chaining（CBC） Mode
在加密前會先與前一個密文做 XOR，第一個密文前面已經沒有東西了，所以會有 Initailization Vector（IV）[^1]
![[W2-3_CBC.png|center]]![[W2-3_CBC-dec.webp|center]]
##### 攻擊手法
如果同時有明文和密文結果，想要插入字串 `Target msg` 到密文中
![[W2-3_bit_flipping.png|center|519]]
- **原理**：把 $\mathsf{Plaintext}$（橘色的部分）$\oplus$ 自己，再 $\oplus \mathsf{Target\ msg}$ 
	> $\mathsf{Plaintext}  \oplus (\mathsf{Plaintext} \oplus \mathsf{Target\ msg}) = \mathsf{Target\ msg}$
- **可操縱部分**：$C_1$ 
-> 將 $C_1' = C_1 \oplus \mathsf{Plaintext} \oplus \mathsf{Target\ msg}$ 作為新的 Cipher 1 （= block 2 的 IV）替換 $C_1$
-> 另一方收到 Block 2 解密後 $\oplus$ $C_1'$ 得到 $\mathsf{Target\ msg}$

## 解題
1. 觀察 source code，發現：
   - 使用 `MODE_CBC` -> blocks 串流 XOR 加密
   - Padding 以十六為單位 -> 一個 block 16 bytes = 32 個字元
   - 可知原始明文和對應的加密結果
   - **目標**：替換密文使內容含有 `wha13.github.io/`
   
   -> Bit flipping attack
1. 寫腳本
   ```python
	r = remote(HOST, PORT)
	r.recvuntil(b"Change the first block into ")
	
	target_msg = r.recvline().strip()
	ori_msg = bytes.fromhex(r.recvline().decode().split(':')[1])
	cipher = bytes.fromhex(r.recvline().decode().split(':')[1])
	 
	r.recv() # One Shot >
	
	#      iv_2 = cipher[1]  -> new cipher_1 = cipher[1] ^ (p_2 ^ target_msg)
	fake_msg = xor(cipher[:16], ori_msg[16:32], target_msg) + cipher[16:32]
	
	r.sendline(fake_msg.hex().encode())
	print(r.recvall().decode())
   ```
   ![[W2-3_flag.png|615]]
1. flag = `FLAG{5f599c3daf5ec712e54fe71f6e71d23f2d6d8cbfb6594bdae6ea7b49a665cf70}`





[^1]: [Day 21. 加密演算法要注意的那些毛 (一) - 加密模式](https://ithelp.ithome.com.tw/m/articles/10249953)
