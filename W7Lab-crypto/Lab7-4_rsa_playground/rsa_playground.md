#Crypto 

## 題目

**rsa_playground**

Three levels in my RSA playground!

並附了兩個檔案，一個放了三個 stages 的 `n`、`c`、`e`，另一個：
```python
	from Crypto.Util.number import *
	flag1=b'REMOVED FLAG'
	flag2=b'REMOVED FLAG'
	flag3=b'REMOVED FLAG'
	flag=flag1+flag2+flag3
	print(flag)
	c1=bytes_to_long(flag1)
	c2=bytes_to_long(flag2)
	c3=bytes_to_long(flag3)
	
	def stage1(c):
	    p, q=getPrime(512), getPrime(512)
	    n=p*q
	    e=3
	    c=pow(c, e, n)
	    print('----------------------------stage1------------------------------')
	    print(f'n:{n}')
	    print(f'c:{c}')
	    print(f'e:{e}')
	
	def stage2(c):
	    p=getPrime(128)
	    q=p+1
	    while isPrime(q)==False:
	        q=q+1 #q will be the next prime number after p
	    n=p*q
	    e=65537
	    c=pow(c, e, n)
	    print('----------------------------stage2------------------------------')
	    print(f'n:{n}')
	    print(f'c:{c}')
	    print(f'e:{e}')
	
	def stage3(c):
	    p, q=getPrime(512), getPrime(512)
	    n=p*q
	    d=getPrime(200)
	    e=inverse(d, (p-1)*(q-1))
	    c=pow(c, e, n)
	    print('----------------------------stage3------------------------------')
	    print(f'n:{n}')
	    print(f'c:{c}')
	    print(f'e:{e}')
	
	stage1(c1)
	stage2(c2)
	stage3(c3)
```


## 解題
1. 觀察 source code，有 3 個 stage，`flag = flag1 + flag2 + flag3`，每個 flag 對應到一個 stage
2. 從 `stage1` 可以看到明顯的 `e` 太小，參考 Lab7-22_eee 的做法，求出 `m1`（flag1）
   ```python
   m1 = long_to_bytes(gmpy2.iroot(c1,e1)[0])
   ```
3. `stage2` 給了提示 `#q will be the next prime number after p`
   `p`、`q` 相近 -> $q \times q \approx n^2$ 
   -> `p`、`q` 為 $\sqrt{n}$ 前後各一個質數 -> `prevprime(`$\sqrt{n}$`)`、`nextprime(`$\sqrt{n}$ `)`
4. `stage3` 的 `d = getPrime(200)`，非常小 -> Wiener’s Attack 近似出 `d`
   ![[W7-4_Wiener’s.png|415]]
   ```python
   # 輾轉相除
	def continued_fraction(a, b):
	    while b:
	        yield a // b
	        a, b = b, a % b
	
	# k / d 的候選值
	def k_d(cf):
	    p0, p1 = 0, 1
	    q0, q1 = 1, 0
	
	    for a in cf:
	        p0, p1 = p1, a * p1 + p0
	        q0, q1 = q1, a * q1 + q0
	
	        yield p1, q1
	
	def wiener(e, N):
	    for k, d in k_d(continued_fraction(e, N)):
	
	        if k == 0:
	            continue
	        if (e * d - 1) % k != 0:
	            continue
	        phi = (e * d - 1) // k
	        
	        s = N - phi + 1 # p + q = N - phi + 1
	        delta = s * s - 4 * N # x² - sx + N = 0
	
	        if delta < 0:
	            continue
	
	        root = isqrt(delta)
	        if root * root == delta:
	            p = (s + root) // 2
	            q = (s - root) // 2
	            if p * q == N:
	                return d
	    return None
	
	d3 = wiener(e3, n3)
	m3 = long_to_bytes(pow(c3, d3, n3))
   ```
1. 最後 `flag = m1 + m2 + m3` 結果是 `b'ICED{U_JuST_D0ne_all_theCh4ll3nges!}'`，看出來 m2、m3 中間少了 `_`，加回去
2. flag = `ICED{U_JuST_D0ne_all_the_Ch4ll3nges!}`
   
