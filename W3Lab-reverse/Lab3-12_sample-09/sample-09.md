#Reverse 

| 選項        | 特徵                                                            | 特徵                                                |
| --------- | ------------------------------------------------------------- | ------------------------------------------------- |
| **TEA**   | - 64-bit block，128-bit key          <br>- 兩個 32-bit word 互相更新 | - 常數 `0x9E3779B9`<br>- 固定 key index               |
| **XTEA**  | TEA 改良版                                                       | - 常數 `0x9E3779B9`<br>- key index 跟 `sum` 的 bit 有關 |
| **XXTEA** | 同時處理多個 32-bit word                                            | array / 多 word 迴圈                                 |
| **AES**   | 128-bit block                                                 | S-box、MixColumns、AES-NI                           |

- TEA
  → key index 固定
  → k0 / k1 / k2 / k3 寫死在運算裡
- XTEA
  → key index 會變
  → 常看到 & 3
  → 常看到 (sum >> 11) & 3
  → 再拿這個 index 去 key array

---
# sample-09

## 題目

Analyze `sample09` and select one option from each group.

| A: Algorithm                                                   | B:  Cycles (1 cycle = 2 half-rounds)                                      | C: Block / Key size                                                                                                                            |
| -------------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| - A1: TEA           <br>- A2: XTEA<br>- A3: XXTEA<br>- A4: AES | - B1: 16 cycles<br>- B2: 32 cycles<br>- B3: 64 cycles<br>- B4: 128 cycles | - C1: 64-bit block / 128-bit key<br>- C2: 64-bit block / 256-bit key<br>- C3: 128-bit block / 128-bit key<br>- C4: 128-bit block / 256-bit key |

## 解題
1. 從程式碼看到，`a1 == 2` -> 兩個 word 
   ```c
   v5 = _byteswap_ulong(dest);
   v6 = _byteswap_ulong(v10);
   for ( i = 0; i != -957401312; v6 += (i + v5) ^ (dword_407C + (v5 >> 5)) ^ (dword_4078 + 16 * v5) ) {
		i -= 1640531527;
		v5 += (v6 + i) ^ (dword_4074 + (v6 >> 5)) ^ (dword_4070 + 16 * v6);
	}
   ```
   - `i -= 1640531527`  -> `sub ecx, 61C88647h`
     在 32-bit 下 `-0x61C88647` = `0xffffffff` - `0x61C88647` = `0x9e3779b8`
     -> TEA or XTEA
   - key 為固定值：`dword_4070`、`dword_4074`、`dword_4078`、`dword_407C` -> TEA
1. cycle 數量：
   ```python
	delta = 0x9E3779B9
	target = 0xC6EF3720
	
	for n in range(1, 100):
	    if (delta * n) & 0xffffffff == target:
	        print(n)
	        break
   ```
   -> 32
1. `v5`、`v6`使用 `_byteswap_ulong()` -> 各為 4 bytes，相加為 64 bit -> block = 64 bits
2. key 為 `dword`，Double Word，佔 4 Bytes（32 bits），四把 -> 128 bits
3. flag = `a1-b2-c1`


---
