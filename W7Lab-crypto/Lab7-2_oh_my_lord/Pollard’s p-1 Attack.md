#Crypto 

## 題目

**oh_my_lord**

~~Is Pollard a king or lord?~~

並附了一個檔案，簡化後：
```python
def gen_special():
    while True:
        cur = 2
        for i in range(30):
            cur *= getPrime(20)
        if isPrime(cur+1):
            return cur+1

p, q = gen_special(), gen_special()
N = p * q
e = 0x10001
c = pow(bytes_to_long(flag) ,e , N)
print(f"{N=}\n{e=}\n{c=}")

# N=1417028082586606812741772936011827684012154181744935910615795205485536664335697241560879552672305783820205657476565585525299974974829864016779337457784883701684378869534602049587092156040559962509466267816478276224450740901161169471463790752944924191633584379258806753435043170117908242919285750823035946739451712102155204085414218700480344038846415769737
# e=65537
# c=872763157460372457481642783011874076012886523071986619947230078967901347191920682724314055615365203666117168987640225396705256288778055978045942459458458543774231060425891735543278103902718884863638076490767560480429542160833756196084959062700453285955377713274542985288269115406606934796766201079211151604973174709021924018399215347590225452861621571335

```

### Pollard’s p-1 Attack
一種分解 RSA 模數 $N = p \times q$ 的方法，適合某個質因數的 $p-1$ 很平滑時
> 平滑：包含很多小質因數，都不大
> 	ex: `p - 1 = 2^4 * 3^2 * 5 * 7`
##### 攻擊手法
1. 找到一個平滑的 $M=k(p-1), \; k \in \mathbb{N}$ 的倍數，利用費馬小定理 $a^{p-1} ≡ 1 \; \texttt{mod} \; p$ 
   -> $a^{k(p-1)} \; \texttt{mod} \; p = 1^k \; \texttt{mod} \; p = 1 \; \texttt{mod} \; p$
   -> $a^M ≡ 1 \; \texttt{mod} \; p$ -> $p \; | \; (a^M - 1)$
2. 求 $\mathsf{gcd}(a^M - 1, N)$ ，如果結果不是 1 也不是 $N$，通常就直接得到 $p$

## 解題
1. 觀察 source code，發現 `gen_special()` 產生由多個小質數相乘的值 `curr`，並回傳 `curr-1` 作為 `p` 和 `q`
2. 題目提到 Pollard -> Pollard's p-1 attack 
   -> 找到 $M$ ，求 $\mathsf{gcd}(a^M - 1, N)$ 不是 1 也不是 $N$ 的結果
3. 選一個和 N 互質的小整數`a`，逐步加入小質數，每次都檢查 gcd
   ```python
   from sympy import primerange
   from math import gcd
   
   a = 2
	for prime in primerange(2, 2**20):
	    a = pow(a, prime, N)
	    p = gcd(a - 1, N)
	
	    if 1 < p < N:
	        q =  N // p
	        break
   ```
1. 得到 `p`、`q` 後用 RSA 解
   ```python
   phi = (p-1)*(q-1)
	d = pow(e, -1, phi)
	print(long_to_bytes(pow(c, d, N)))
   ```
2. flag = `FLAG{it_is_also_cool_to_learn_about_williams_approach}`
   
