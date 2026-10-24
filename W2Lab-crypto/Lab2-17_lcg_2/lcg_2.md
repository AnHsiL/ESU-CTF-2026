#Crypto

## 題目

**lcg_2**  
Something missing...

`nc 45.77.20.255 31016`
並提供了 source code，簡化後：

```python
p = getPrime(256)
a, b = 0x120, 0x1337

def lcg(x):
    return (a*x + b) % p

seed = int.from_bytes(os.urandom(32), 'little')
cur = lcg(seed)

while input("> ") == 'next':
    print("now:", cur)
    cur = lcg(cur)

if int(input("ans: ")) == cur:
    print(flag)

else:
    print("failed qwq")
```



---

## 解題

1. 觀察 source code，這次沒有提供 `p`
2. 利用性質 $\mathsf{gcd} (aX_0 + b - x_1,\;\; ax_1 + b - x_2,\;\; ...) = p$ 得出 `p`
   ```python
   p = math.gcd(a*p1 + b - p2, a*p2 + b - p3)
   ```
3. 腳本：
   ```python
	r = remote(HOST, PORT)
	r.sendlineafter("> ", b'next')
	r.recvuntil(b"now: ")
	p1 = int(r.recvline().strip())
	
	r.sendlineafter("> ", b'next')
	r.recvuntil(b"now: ")
	p2 = int(r.recvline().strip())
	
	r.sendlineafter("> ", b'next')
	r.recvuntil(b"now: ")
	p3 = int(r.recvline().strip())
	
	a, b = 0x120, 0x1337
	p = math.gcd(a*p1 + b - p2, a*p2 + b - p3)
	
	def lcg(x):
	    return (a*x + b) % p
	
	cur = f'{lcg(p3)}'
	r.sendlineafter(b"> ", b"stop")
	r.sendlineafter("ans: ", cur.encode())
	
	print(r.recvline().decode())
   ```
1. flag = `FLAG{4d64385ac3d209e576cefc63cd5d9fd070e69ddb482ef1b5f4860c29b1c8eb89}`


