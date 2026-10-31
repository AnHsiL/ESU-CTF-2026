#Crypto

## 題目

**normal_19937**  

`nc 45.77.20.255 31019`
並提供了 source code，簡化後：

```python
while input("> ") == "next":
    print("next:", getrandbits(1337))

if int(input("ans: ")) == getrandbits(1337):
    print(flag)
```


---

## 解題
1. 觀察題目和 source code，大致上與 [[baby_19937#題目| baby 19937]] 一樣，但 `getrandbits(1337)` 每次產生 41 個完整 32-bit 輸出 + 25 bits
   -> 每個不完整輸出少 7 bits -> MT state 無法直接 `untemper`
2. 蒐集題目資訊
   ```python
   for _ in range(ROUNDS):
	    r.sendlineafter(b"> ", b"next")
	    value = int(r.recvline().decode().split(": ", 1)[1])
	
	    # 41 個 32-bit chunks
	    for i in range(OUTPUT_NUM):
	        outputs.append((value >> (32 * i)) & MASK32)
	        masks.append(MASK32)
	
	    # ...25 bits
	    last_25 = ( value >> (32 * OUTPUT_NUM) ) & ((1 << LAST_BITS) - 1)
	
	    outputs.append(last_25 << 7)
	    masks.append(MASK32 ^ 0x7f)
	
	states = [untemper(out) for out in outputs[:624]]
	unknown = []
	for i in range(624):
	    if masks[i] != MASK32:
	        for bit in range(7):
	            unknown.append((i, bit))
	            
	count = len(outputs) - 624
	
	MT = init_mt(states)
	base = [MT.rand() for _ in range(count)]
   ```
1. 把已知 bits `untemper`，未知的 7 bits 暫時視為 0
   - 用 MT19937 的 `tempering`、`twist` 分別測試每個未知 bit 的輸出
     ```python
	   effects = []
		for pos, bit in unknown:
		    test_states = states.copy()
		    test_states[pos] ^= untemper(1 << bit)
		
		    MT_test = init_mt(test_states)
		
		    effect = [  MT_test.rand() ^ base[i]  for i in range(count) ]
		    effects.append(effect)
	   ```
   - 用輸出建立 GF(2) 線性方程組
     ```python
     equations = []
	for i in range(count):
	    target = outputs[624 + i]
	    mask = masks[624 + i]
	    diff = (target ^ base[i]) & mask
	
	    for bit in range(32):
	        if not (mask & (1 << bit)):
	            continue
	
	        row = 0
	        for j in range(len(unknown)):
	            if effects[j][i] & (1 << bit):
	                row |= 1 << j
	
	        rhs = (diff >> bit) & 1
	        equations.append((row, rhs))
     ```
   - 用 Gaussian elimination 求出缺少的 bits，補回完整 624 個 state
     ```python
		solution = solve_gf2(equations, len(unknown))
		for j, (pos, bit) in enumerate(unknown):
			if solution & (1 << j):
			states[pos] ^= untemper(1 << bit)
		
		# 驗證恢復結果
		MT = init_mt(states)
		for i in range(count):
			predicted = MT.rand()
			actual = outputs[624 + i]
			mask = masks[624 + i]
			
			assert (predicted & mask) == actual, (
				f"Mismatch at output {624 + i}"
			)
		```
	
1. 預測下一個 `getrandbits(1337)`
   ```python
	ans = 0
	for i in range(OUTPUT_NUM):
	    ans |= MT.rand() << (32 * i)
	
	ans |= (MT.rand() >> 7) << (32 * OUTPUT_NUM)
   ```
2. flag = `FLAG{90a937f1e8923565df0ef1d39fa96f6505e43aeca1459c74ae3b35a91cb860cc}`


