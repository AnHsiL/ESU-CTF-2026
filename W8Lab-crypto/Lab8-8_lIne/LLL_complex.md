#Crypto 

## 題目

**lIne**

【THJCC 2025】 lIne
Complex numbers and LLL

並附了檔案 `chal.py`：
```python
from sage.all import CC

flag=os.urandom(8).hex()
keys=[getrandbits(48) for _ in range(16)]

def to_complex(datas):
    imag_datas=[]
    for i in range(0, len(datas), 2):
        imag_datas.append(CC([datas[i], datas[i+1]]))
    return imag_datas

imag_flag=to_complex([int(chr, 16) for chr in flag])
imag_keys=to_complex(keys)

cnt=0
for i in range(8):
    cnt+=imag_flag[i]*imag_keys[i]

print(f"{imag_keys}\n{cnt}")
print(f"Gift: {hashlib.md5(b'THJCC{'+flag.encode()+b'}').hexdigest()}")

# [9.83329568728950e13 + 1.94539067458416e14*I, 4.57795946512170e13 + 5.54913449090490e13*I, 3.35752608137010e13 + 1.10651091133529e14*I, 8.09172050820060e13 + 6.09012985967910e13*I, 2.75388068605530e13 + 5.12867910525740e13*I, 2.33510497525684e14 + 9.11264352204540e13*I, 2.36186170290599e14 + 2.03323868604921e14*I, 1.37793863865401e14 + 1.40354868241912e14*I]
# 3.22421607806873e14 + 1.37668712938916E+16*I
# Gift: 69ae60327282356b2f2731e6acf624f4
```

## 解題
(程式碼皆寫在 `.sage`)
1. 觀察 `chal.py`
	1. flag 拆成 hex 小字元 -> `to_complex()` 每兩個數組成一個複數（實部+虛部）
	   ```
	   [a0, a1, a2, a3, ...]
		→
		[a0 + a1*i, a2 + a3*i, ...]
	   ```
   2. keys `to_complex()`  把 16 個 48-bit 大整數，兩兩組成 8 個複數 
      ```
      imag_keys = [
		    k0 + k1*i,
		    k2 + k3*i,
		    ...
	]
      ```
    3. `cnt` = `imag_key` × `imag_flag` 的線性組合
    4. `Gift` 候選 flag 算 MD5 驗證答案
3. 從題目的 `cnt+=imag_flag[i]*imag_keys[i]`可以推導出 $\text{coeff}_{real}$、$\text{coeff}_{imag}$
   $$(f[i]_r+f[i]_i*I)(k[i]_r+k[i]_i*I)\\
   =(f[i]_r \times k[i]_r-f[i]_i \times k[i]_i)+(f[i]_r\times k[i]_i+f[i]_i \times k[i]_i)*I$$ 
   ```python
   coeff_r = []
	coeff_i = []
	
	keys = [
	    (ZZ(RR(k).round()), ZZ(RR(k_i).round())) for k, k_i in imag_keys
	]
	for k, k_i in keys:
	    coeff_r += [k, -k_i]
	    coeff_i += [k_i, k]
   ```
   
   因此：
   $$\sum{(\text{coeff}_{real}[i] * f_i)} ≈ cnt_{real}$$
   $$\sum{(\text{coeff}_{imag}[i] * f_i)} ≈ cnt_{imag}$$ 
3. 令 $S$ 為 scale、$R_i=\text{coeff}_{real}[i]$、$I_i=\text{coeff}_{imag}[i]$，將係數轉換成矩陣：
   $$ A=
   \begin{pmatrix}
	S & 0 & \cdots & 0 & R_0 & I_0\\
	0 & S & \cdots & 0 & R_1 & I_1\\
	\vdots & & \ddots & \vdots & \vdots & \vdots\\
	0 & 0 & \cdots & S & R_{15} & I_{15}
	\end{pmatrix}$$
	```python
	SCALE = 1000 # 可調整的權重

	A = [[0]*18 for _ in range(16)]
	
	for i in range(16):
	    A[i][i] = SCALE
	    A[i][-1] = coeff_i[i]
	    A[i][-2] = coeff_r[i]
	
	A = Matrix(ZZ, A)
	```
	
	發現特徵：
   - flag 小字元  → 小
   - coeff  → 大 
   
   -> 符合 LLL 特徵 "已知很大的係數 + 相對很小的未知數" 
1. 依照矩陣的邏輯，目標希望
   - 後兩維接近 $cnt_{real}$、$cnt_{imag}$ 
   - 前 16 維（$f_i$）接近 scale$\times f[i]$ 的中心 $S \times 7.5$
     >note: $f[i] \in [0, 15]$ -> 前 16 維目標為 $S\times \frac{\sum_i{f[i]}}{16} = S \times 7.5$ 

	```python
	target = vector(
	    ZZ,
	    [SCALE*(0+15)//2]*16 + [cnt_r, cnt_i]
	)
	```
1. 找 Closest Vector Problem（CVP）找到的 lattice vector $v=S\cdot f[i]$
   ```python
   # CVP: LLL + Babai nearest plane
	B = A.LLL()
	
	# Gram-Schmidt
	B_QQ = Matrix(QQ, B)
	G, _ = B_QQ.gram_schmidt(orthonormal=False)
	
	# Babai nearest plane：找接近 target 的 lattice vector
	y = vector(QQ, target)
	v = vector(ZZ, [0]*18)
	
	for i in reversed(range(B.nrows())):
	    c = ZZ(round((y * G[i]) / (G[i] * G[i])))
	    v += c * B[i]
	    y -= c * B_QQ[i]
   ```
1. 把 CVP 找到的 lattice vector v 前 16 維，還原成原本的 flag 小字元，再組合成完整 flag
   ```python
   flag_part = [v[i] // S for i in range(16)]
   
	if all(0 <= x <= 15 for x in flag_part):
		flag = "".join(hex(x)[2:] for x in flag_part)
		print(hashlib.md5(b"THJCC{" + flag.encode() + b"}").hexdigest() == Gift)
		print("THJCC{" + flag + "}")
   ```
1. flag = `THJCC{767da19058a53add}`
   
