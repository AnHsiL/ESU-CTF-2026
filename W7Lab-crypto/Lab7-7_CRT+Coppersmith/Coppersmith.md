#Crypto 

## 題目

**brokencast**

CRT with errors. Coppersmith may help!

並附了兩個檔案，一個放了多個 p、c，另一個簡化後：
```python
assert len(flag) == 84

e = 0x10001
output = ''

def encrypt(msg):
    print(msg)
    global output
    m = bytes_to_long(msg)
    p = getPrime(20)
    c = pow(m, e, p)
    output += f"{p=}\n{c=}\n"

all_msg = []

for i in range(80):
    all_msg.append(flag)
    all_msg.append(os.urandom(84))

random.shuffle(all_msg)

for msg in all_msg:
    encrypt(msg)

f = open('output.txt', 'w')
f.write(output)
f.close()
```

### Coppersmith
尋找模多項式所有小整數根的方法，透過 LLL 把原本難解的模多項式，轉成一個在整數域上比較容易找根的多項式

例如 RSA $c = m^e \pmod N$，當明文大部分已知時 `m = known || x`，把已知部分標為 $m_0$： $$m = m_0 + x$$
建立 $f(x)=(m_0+x)^e-c \equiv 0\pmod N$ ，找 $x$

## 解題
1. 觀察 source code，發現程式將 80 個 flag 和 80 個亂數打亂加密成輸出，每組都使用不同的 20-bit prime $p_i$，最後提供每個的密文和模數
2. 全部用中國餘式定理（CRT）解
	1. 每組 ciphertext 解回餘數
	   $$d_i=e^{-1}\mod (p_i-1)$$ $$r_i=c_i^{d_i}\bmod p_i$$ 
	   ```python
	   residues = []
		for p, c in zip(moduli, cipher):
		    d = inverse_mod(e, p-1)
		    r = power_mod(c, d, p)
		    residues.append(r)
	   ```
	2. 對 residue 做 CRT
	   ```python
	   N = prod(moduli)
		R = CRT(residues, moduli)
	   ```
3. 轉成 Coppersmith small root，建立 $f(x)=x-R$ 並找出根使 $f(x)\equiv0\pmod P$ 
   ```python
   FLAG_BITS = 84 * 8 
	BETA = 0.45
   PR.<x> = PolynomialRing(Zmod(N))
	f = x - R       # Coppersmith
	
	roots = f.small_roots(
	    X=2^FLAG_BITS,
	    beta=BETA,
	    epsilon=0.03
	)
	
	print(long_to_bytes(int(roots[0])))
   ```
   > 如果 beta=0.5，可找的 root 大小上限接近 $X < N^{\beta^2-\epsilon}$
   
1. flag = `FLAG{congr8s_u_solved_the_hardest_problem_in_that_year_also_lll_is_cool_to_know_owo}`
   
