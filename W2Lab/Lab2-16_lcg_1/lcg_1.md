#Crypto

## 題目

**lcg_1**  
Just some simple simple math!

`nc 45.77.20.255 31015`
並提供了 source code，簡化後：

```python
p = 2**255 - 19
a, b = 0x120, 0x1337

def lcg(x):
    return (a*x + b) % p

seed = int.from_bytes(os.urandom(32), 'little')
cur = lcg(seed)
print("now:", cur)
cur = lcg(cur)

if int(input("ans: ")) == cur:
    print(flag)

else:
    print("failed qwq")
```

### LCG
是個產生偽隨機數的方法[^1]
$$X_{n+1} = (aX_n + c) \;\mathsf{mod}\; m$$
特性：
$$\mathsf{gcd} (aX_0 + c - x_1,\;\; ax_1 + c - x_2,\;\; ...) = m$$

---

## 解題

1. 觀察 source code -> 只要傳回 `lcg(now)` 就可以了
2. 腳本：
   ```python
	r = remote(HOST, PORT)
	r.recvuntil("now: ")
	now = int(r.recvline().strip())
	
	cur = f'{lcg(now)}'
	r.sendlineafter("ans:", cur.encode())
	
	print(r.recvline().decode())
   ```
1. flag = `FLAG{b48c6d97e0623d322261e92b344d5b7d04cb9790bdfdd7b77d15d9e823ebe026}`



[^1]: [06 Random Number Generation.pptm](https://www.mi.fu-berlin.de/inf/groups/ag-tech/teaching/2012_SS/L_19540_Modeling_and_Performance_Analysis_with_Simulation/06.pdf)
