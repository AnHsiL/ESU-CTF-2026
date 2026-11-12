#Crypto 

## 題目

**flying_rabbit**

我看到兔子在飛 owo

並附了兩個檔案，一個放了 `e`、 `n`、`a`、`b`、`c1`、`c2`，另一個：
```python
from Crypto.Util.number import *
flag = b'SECRET{SECRET_SECRET_SECRET}'
a = 1004
b = 120
m1 = bytes_to_long(flag)
m2 = a*m1 + b
p, q = getPrime(1024), getPrime(1024)
e = 7
n = p*q
c1 = pow(m1, e, n)
c2 = pow(m2, e, n)
print(f"{e=}\n{n=}\n{a=}\n{b=}\n{c1=}\n{c2=}")
```

### Franklin-Reiter Attack
有兩個 RSA 密文，而且兩個明文之間有已知的線性關係時，可以改寫成兩個多項式，並求出含有明文訊息的公因數
例如：
```python
m2 = a*m + b
```
密文：
```python
c1 =         m ^ e mod n
c2 = (a*m + b) ^ e mod n
```
改寫成多項式：
```python
f(x) = x^e - c1
g(x) = (a*x + b)^e - c2
```
明文 $m$ 代進去時，$f(m) = g(m) = 0$
-> 都有因數 $(x-m)$ 
-> $\mathsf{gcd}(f(x), \; g(x)) = x-m$
-> 求 $m$

## 解題
1. 觀察 source code，發現 `m1`、`m2` 有線性關係 $m_2 = a \times m_1 + b$ -> Franklin-Reiter Attack
2. 因為含有複雜的多項式、域關係，到 [sega cell server](https://sagecell.sagemath.org/) 執行
   ```sega
   e = ...
	n = ...
	a = ...
	b = ...
	c1 = ...
	c2 = ...
   def poly_gcd(f, g):
	    while g:
	        f, g = g, f % g
	    return f.monic()
	
	R.<x> = Zmod(n)[]
	f = x^e - c1
	g = (a*x + b)^e - c2
	
	h = poly_gcd(f, g)
	m = -h[0]
	
	print(int(m))
   ```
1. 結果拿回到 python 
   ```python
   from Crypto.Util.number import long_to_bytes
	m = [sega 結果]
	print(long_to_bytes(m))
   ```
2. flag = `ICED{F-R=Flying-R4bb1t_or_Franklin-Reiter_w3ll..._nevermind_but_shark_is_the_cutiest!!!}`
   
