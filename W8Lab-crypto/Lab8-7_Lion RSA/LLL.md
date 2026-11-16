#Crypto 

## 題目

**Lion RSA**

【NoHackNoCTF 2024】 Lion RSA
Recover three RSA primes from a modular linear leak with LLL.

並附了兩個檔案，`output.txt`、`chal.py`：
```python
def leak_info(primes):
    mod = getPrime(4096)
    parameters = [getPrime(4096) for _ in range(3)]
    cnt = sum(primes[i] * parameters[i] for i in range(3)) % mod
    print(f"---leak info---\n{cnt=}\n{parameters=}\n{mod=}")

primes = [getPrime(512) for _ in range(3)]
p, q, r = primes
n = p * q * r
e = 0x10001   # 65537
c = pow(bytes_to_long(flag2), e, n)
print(f"{n=}\n{e=}\n{c=}")
leak_info(primes)
```

### LLL
LLL（Lenstra–Lenstra–Lovász）：把一組很亂、很長的格點基底，換成一組較短、接近正交的基底，讓「係數很小、彼此有關係的整數解」更容易被找出來
>[!abstract] 正交基底
>![[Gram Schmidt.png|600]]

![[LLL.png|center|593]]
##### 流程
1. 對 input lattice vector 做 **Gram-Schmidt**，看各向量彼此重疊多少。
2. 做 scaling 相減，例如 $$b_i \leftarrow b_i-\text{round}(\mu_{i,j})b_j$$ 把可以用前面向量消掉的部分消掉，使向量變短
3. 檢查 Lovász condition。把比較短的向量往前排
4. 直到出來的值小於給定的 δ return B
##### 在 CTF 的特徵
已知一些很大的係數，但未知數相對很小 → 想辦法把方程式塞進 lattice 
→ 用 LLL 找短向量 → 短向量裡可能藏著未知數。

## 解題
1. 觀察 `chal.py`，程式在執行三質數 RSA 後，額外洩漏 `cnt`、`parameters = [a, b, c]`、`mod` 
   -> 可以推導出 $ap+bq+cr \equiv cnt \pmod{mod}$
   其中：
   - p, q, r       ≈ 512 bit    ← 很小
   - a, b, c, mod   ≈ 4096 bit   ← 很大
   
   -> 符合 LLL 特徵 "已知很大的係數 + 相對很小的未知數" -> 可以建成 lattice
1. 用 sage 解
   - WSL+sage 安裝（sage 支援 ubuntu 22.04 以下的系統）
     【WSL2 install】
		```bash
		wsl --install -d Ubuntu-22.04
		```
		【WSL2 啟動】
		```bash
		wsl -d Ubuntu-22.04
		```
		【sage install】
		```bash
		sudo apt update
		sudo apt install sagemath
		```
   
   `solve.sage`：
   ```python
   A = [[0]*5 for _ in range(5)]
	for i in range(3):
	    A[i][-1] = -parameters[i]
	    A[i][i] = 1
	
	A[3][-1] = cnt
	A[3][3] = pow(2, 4096)
	A[4][-1] = mod
	
	A = Matrix(ZZ, A)
	lll = A.LLL()
	
	for v in lll:
	    if v[-1] == 0:  # RSA
	        p, q, r = int(v[0]), int(v[1]), int(v[2])
	        phi = (p-1)*(q-1)*(r-1)
	        d = pow(e, -1, phi)
	        print(long_to_bytes( pow(int(c), int(d), int(n))) )
   ```
   執行
   ```bash
   sudo sage solve.sage
   ```
1. flag = `NHNC{three_baby_lions_math_won}`
   
