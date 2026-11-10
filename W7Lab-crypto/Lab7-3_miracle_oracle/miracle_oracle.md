#Crypto 

## 題目

**miracle_oracle**

What does an oracle actually mean ...

並附了 nc 連線和一個檔案，簡化後：
```python
p, q = getPrime(1024), getPrime(1024)
N = p*q
e = 0x10001 # 65537
d = inverse(e, (p-1) * (q-1))
c = pow(bytes_to_long(flag), e, N)
print(f"{N=}\n{c=}")

while True:
    new_c = int(input("> "))
    print(f"< {pow(new_c, d, N) & 1}")
```

### RSA LSB Oracle
有 rsa 解密，但只能取得最後 1 bit (LSB)
攻擊方法：用 Binary Search 縮小範圍，逼近明文
![[W7-3_LSBOracle.png|center|573]]
##### 演算法
```pseudocode
Step1: [L, R] = [0, N]
Step2: 
	for i in range ⌈log2 n⌉, do:
		c = c*(2^e) mod N
		if LSB(c) = 0 -> m in [L, (L+R)/2]
		elif LSB(c) = 1 -> m in [(L+R)/2, R]
Step3: msg = ⌈L⌉ = ⌊R⌋
```

## 解題
1. 觀察 source code，發現程式會提供 N 和密文 `c`，隨後將輸入的密文用 RSA 解密，並輸出最後一個 bit -> RSA LSB Oracle Attack
2. 寫腳本
   ```python
   multiplier = pow(2, e, N)
	L = Fraction(0)
	R = Fraction(N)
	
	for _ in range(N.bit_length()):  # bit_length() = floor(log2(N))+1
	    c = c * multiplier % N
	    r.sendlineafter("> ", str(c).encode())
	    isOdd = int(r.recvline().decode().split('< ')[1])
	    mid = (L + R) / 2
	
	    if isOdd:
	        L = mid
	    else:
	        R = mid
	
	print(long_to_bytes(int(R)))
   ```
1. flag = `FLAG{d08104b6010614db2fbeb27fd4253a89982776d29aab37496fdb29f364e46d83}`
   
