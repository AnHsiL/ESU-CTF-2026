#Crypto

## 題目

**lcg_3**  
This is not easy at all, the truncated LCG Problem!

`nc 45.77.20.255 31017`
並提供了 source code，簡化後：

```python
p = 2**255 - 19
a, b = 0xdeadbeefcafebabe123456789abcdef0, 0

def lcg(x):
    return (a*x + b) % p

seed = int.from_bytes(os.urandom(32), 'little')
cur = lcg(seed)

for _ in range(16):
    if input("> ") != 'next':
        break
    print("now:", cur>>192)
    cur = lcg(cur)

if int(input("ans: ")) == cur:
    print(flag)
else:
    print("failed qwq")

```

### Truncated LCG
LCG 產生亂數後，只公開其中一部分 bits，隱藏其餘 bits
假設 LCG $X_{n+1}=(aX_n+b)\bmod p$ 生成 16-bit 的數字，Truncated LCG 可能只公開高 8 bits，攻擊者視角：
```
X1 = 10110110 ????????
X2 = 01101001 ???????? 
X3 = 11001011 ????????
```

#### 攻擊方法 - LLL 的應用
Lenstra–Lenstra–Lovász（LLL） 是一種 Lattice Reduction 演算法，可以將一組長且雜亂的 Lattice Basis 轉換成「短且接近正交」的 basis

假設生成 16-bit 數字，用 $K_i$ 表示已知的 8 bits，$e_i$ 表示未知的 8 bits，
將 Truncated LCG 的結果 $X_i$ 表示為：
$$
X_i=K_i\cdot 2^8+e_i
$$
帶回 LCG 公式中：
$$
X_{i+1} = K_{i+1}\cdot2^8+e_{i+1}\equiv a(K_i\cdot2^8+e_i)+b\pmod p 
$$
把未知項整理後：
$$
e_{i+1}-ae_i\equiv (aK_i-K_{i+1})\cdot2^8+b\pmod p 
$$
嘗試還原 $e_1$、$e_2$、$e_3$ ...

---

## 解題

1. 觀察 source code，題目每次會提供 `cur >> 192` 的 LCG
2. 題目中 $b$ = 0 -> 
	   $X_1=aX_0 \mathsf{mod} p$
	   $X_2=aX_1 = a^2X_0 \mathsf{mod} p$
	   $X_3=aX_2 = a^3X_0 \mathsf{mod} p$
	   $X_2=aX_1 = a^2X_0 \mathsf{mod} p$
  
	帶入： $e_{i+1}-ae_i\equiv (aK_i-K_{i+1})\cdot2^{hide}+b\pmod p$
	->   $e_{i}\equiv a^ie_0 + (a^iK_02^{hide}-K_i2^{hide}) \pmod p$
	可以先把已知的值 $a^i$ 和 `offset` =  $a^iK_02^{hide}-K_i2^{hide}$ 算出來
	```python
	ai = [pow(a, i, p) for i in range(n)]
	offsets = [ (ai[i]*known[0]*hide - known[i]*hide) % p for i in range(n) ]
	```
1. 建立 Lattice & 執行 LLL：建議讓 GPT 寫
2. 還原出 $X_1$ 了之後，LCG 往後推到 $X_{17}$
   ```python
   cur = X1
	for _ in range(16):
	    cur = lcg(cur)
	
	r.sendlineafter(b"ans: ", str(cur).encode())
	print(r.recvall().decode())
   ```
1. flag = `FLAG{f859104eafb85fcd4678bb05af9178367fa8fa9599c45890b8329f4ffc742980}`


