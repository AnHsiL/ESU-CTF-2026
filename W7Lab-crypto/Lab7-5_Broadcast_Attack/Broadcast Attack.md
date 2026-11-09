#Crypto 

## 題目

**louder_louder_one_more_time_plz**

OK, fine, let's broadcast to everyone three times!

並附了一個檔案，簡化後：
```txt
c=710...
e=3
N=9276317...
e=3
N=172781...
e=3
N=1360955...
```

### Broadcast Attack
RSA 在「同一份明文，用相同的小指數 `e`，但不同 `N` 加密」時，如果 `e` = n，而且有至少 n 組不同的 `N`
> 例如同一個 `m` 被送給 3 個人
> ```
> c1 = m^e mod N1
> c2 = m^e mod N2
> c3 = m^e mod N3
> ```

-> 可以用中國剩餘定理 (CRT) 找 x，使
```
x ≡ c1 (mod N1)
x ≡ c2 (mod N2)
...
x ≡ cn (mod Nn)
```
$x = m^e$ ->開 $e$ 次方根 $\mathsf{mod} \; (\prod_{n} N_n)$ 就能得到明文
```
m^e mod (N1*N2*N3*...*Nn)
```

## 解題
1. 觀察 source code，發現提供 3 組密文和 N，並且公鑰 `e` = 3 -> Broadcast Attack
2. 用中國剩餘定理 (CRT) 找 x
   ```python
   N = N1 * N2 * N3
	M1 = N // N1
	M2 = N // N2
	M3 = N // N3
	
	x = (
	    c1 * M1 * inverse(M1, N1) +
	    c2 * M2 * inverse(M2, N2) +
	    c3 * M3 * inverse(M3, N3)
	) % N
   ```
1. 開 $e$ = 3 次方根，得到 flag
   ```python
   m = gmpy2.iroot(x, 3)[0]
	print(long_to_bytes(m))
   ```
2. flag = `FLAG{hanxin_said_gooooood}`
   
