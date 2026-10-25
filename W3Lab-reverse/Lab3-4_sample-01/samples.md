#Reverse 


| 演算法          | 逆向常見特徵                                                                           | 辨識                                                  |
| ------------ | -------------------------------------------------------------------------------- | --------------------------------------------------- |
| **Salsa20**  | - 大量 `ADD + XOR + ROTATE`  <br>- 16 個 32-bit state、64-byte block                 | - Rotate 7, 9, 13, 18  <br>- 常見 `expand 32-byte k`  |
| **ChaCha20** | - 大量 `ADD + XOR + ROTATE`  <br>- 16 個 32-bit state、64-byte block                 | - Rotate 16, 12, 8, 7                               |
| **AES**      | - 16-byte block  <br>- S-box、SubBytes/MixColumns  <br>- (or) 大量 128-bit XMM/SIMD | - AES-NI 指令：`aesenc`、`aesenclast`、`aeskeygenassist` |
| **RC4**      | - 256-byte `S[256]`  <br>- index 累加  <br>- byte swap 很頻繁                         | `S[i]` / `S[j]` 不斷交換，常見 `% 256`                     |

---
# sample-01

## 題目

Analyze `sample01` and select one option from each group.

| A: Algorithm                                                                         | B: Rounds                                                                                           | C: Key size                                                                               |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| - A1: Salsa20                           <br>- A2: ChaCha20<br>- A3: AES<br>- A4: RC4 | - B1: 8 rounds                            <br>- B2: 12 rounds<br>- B3: 20 rounds<br>- B4: 24 rounds | - C1: 64-bit                          <br>- C2: 128-bit<br>- C3: 192-bit<br>- C4: 256-bit |

Submit your choices in A, B, C order as `a<number>-b<number>-c<number>`. For example, A4, B1, C2 → `a4-b1-c2`.

## 解題
1. IDA 打開 `sample` 分析，發現 main 中有一個迴圈頻繁出現 ROTATE
   ```c
   do{
		v17 = v42 ^ __ROL4__(v8 + v13, 7);
		v36 = v7 ^ __ROL4__(v8 + v17, 9);
		v37 = v13 ^ __ROL4__(v17 + v36, 13);
		v18 = v8 ^ __ROR4__(v36 + v37, 14);
		v19 = v14 ^ __ROL4__(v10 + v9, 7);
		v20 = __ROL4__(v19 + v9, 9);
		v21 = v10 ^ __ROL4__(v19 + (v3 ^ v20), 13);
		v38 = v3 ^ v20;
		v22 = v9 ^ __ROR4__(v21 + (v3 ^ v20), 14);
		v23 = v16 ^ __ROL4__(v11 + v15, 7);
		v24 = v39 ^ __ROL4__(v23 + v15, 9);
		v25 = v11 ^ __ROL4__(v23 + v24, 13);
		v26 = v15 ^ __ROR4__(v24 + v25, 14);
		v27 = HIDWORD(v39) ^ __ROL4__(v12 + v41, 7);
		v28 = v40 ^ __ROL4__(v27 + v12, 9);
		v29 = v41 ^ __ROL4__(v27 + v28, 13);
		v30 = v12 ^ __ROR4__(v28 + v29, 14);
		v10 = v21 ^ __ROL4__(v18 + v27, 7);
		LODWORD(v39) = v24 ^ __ROL4__(v18 + v10, 9);
		HIDWORD(v39) = v27 ^ __ROL4__(v10 + v39, 13);
		v8 = v18 ^ __ROR4__(HIDWORD(v39) + v39, 14);
		v11 = v25 ^ __ROL4__(v17 + v22, 7);
		v40 = v28 ^ __ROL4__(v22 + v11, 9);
		v42 = v17 ^ __ROL4__(v11 + v40, 13);
		v9 = v22 ^ __ROR4__(v42 + v40, 14);
		v41 = v29 ^ __ROL4__(v19 + v26, 7);
		v7 = v36 ^ __ROL4__(v26 + v41, 9);
		v14 = v19 ^ __ROL4__(v41 + v7, 13);
		v15 = v26 ^ __ROR4__(v7 + v14, 14);
		v13 = v37 ^ __ROL4__(v23 + v30, 7);
		LODWORD(v3) = v38 ^ __ROL4__(v30 + v13, 9);
		v16 = v23 ^ __ROL4__(v13 + v3, 13);
		v12 = v30 ^ __ROR4__(v3 + v16, 14);
		--v43;
	  }
	  while ( v43 != 0 );
   ```
   -> 懷疑 Salsa20、ChaCha20
   -> rotate 的數字為 `ROL 7`、`ROL 9`、`ROL 13`、`ROR 14`
   -> `__ROR4__ 14` 表示把 14 進行 4 bytes = 32 bits 的向右 rotate
   ->  `ROR 14` = `ROL (32-14)` = `ROL 18`
    ROTATE 7, 9, 13, 18  -> Salsa20 
2. Salsa20 的 state 是 16 個 word，一個 round 會做 4 個 quarter-round，每個 quarter-round 會操作 4 個 word
   -> 把 `do{}` 裡面依照 4 個 quarter-round 的分區，共兩個 round
   -> `do{}` 共執行 `v43` = 10 次
   -> 共有 $2 \times 10 = 20$ rounds 
3. 檢查 `main()` 發現疑似 key size 的數字
   ![[W3-4_keySize.png|289]]
   轉成 hex，x86 / x86_64 硬體架構記憶體採用 Little Endian -> `.to_bytes(4, "little")`
   ```python
	nums = [
		1634760805,
		857760878,
		2036477234,
		1797285236,
	]
	for x in nums:
		print(x.to_bytes(4, "little"))
   ```
   -> 結果組合起來為 b'expand 32-byte k'
   -> 32 bytes = 256 bits
4. flag = `a1-b3-c4`

---

# sample-02