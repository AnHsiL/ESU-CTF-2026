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

## 題目

Analyze `sample02` and select one option from each group.

| A: Algorithm                                                            | B:  Variant / Nonce                                                                                                                       | C: Key size                                                                      |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| - A1: Salsa20              <br>- A2: ChaCha20<br>- A3: AES<br>- A4: RC4 | - B1: Original ChaCha20 (64-bit nonce)      <br>- B2: IETF / RFC 8439 (96-bit nonce)<br>- B3: XChaCha20 (192-bit nonce)<br>- B4: No nonce | - C1: 64-bit                 <br>- C2: 128-bit<br>- C3: 192-bit<br>- C4: 256-bit |
## 解題
1. IDA 打開 `sample` 分析，發現 main 中有一個迴圈頻繁出現 ROTATE
   ```c
	do {
		v19 = v5 + v8;
		v20 = __ROL4__(v19 ^ v7, 16);
		v21 = v20 + v6;
		v22 = __ROL4__(v21 ^ v5, 12);
		v23 = v22 + v19;
		v24 = __ROL4__(v23 ^ v20, 8);
		v68 = v24 + v21;
		v71 = __ROL4__((v24 + v21) ^ v22, 7);
		v25 = v10 + v9;
		v26 = __ROL4__(v25 ^ v11, 16);
		v27 = v26 + v12;
		v28 = __ROL4__(v27 ^ v10, 12);
		v29 = v28 + v25;
		v30 = __ROL4__(v29 ^ v26, 8);
		v31 = v27 + v30;
		v32 = __ROL4__((v27 + v30) ^ v28, 7);
		v33 = v69 + v13;
		v34 = __ROL4__(v33 ^ v14, 16);
		v35 = v34 + v15;
		v36 = __ROL4__(v35 ^ v69, 12);
		v37 = v36 + v33;
		v38 = __ROL4__(v37 ^ v34, 8);
		v39 = v38 + v35;
		v40 = __ROL4__(v39 ^ v36, 7);
		v41 = __ROL4__((v16 + v70) ^ v18, 16);
		v42 = v41 + v17;
		v43 = __ROL4__(v42 ^ v16, 12);
		v44 = v43 + v16 + v70;
		v45 = __ROL4__(v44 ^ v41, 8);
		v46 = v45 + v42;
		v47 = __ROL4__(v46 ^ v43, 7);
		v48 = v32 + v23;
		v49 = __ROL4__(v48 ^ v45, 16);
		v50 = v49 + v39;
		v51 = __ROL4__(v50 ^ v32, 12);
		v8 = v51 + v48;
		v18 = __ROL4__(v8 ^ v49, 8);
		v15 = v18 + v50;
		v10 = __ROL4__(v15 ^ v51, 7);
		v52 = v40 + v29;
		v53 = __ROL4__(v52 ^ v24, 16);
		v54 = v53 + v46;
		v55 = __ROL4__(v54 ^ v40, 12);
		v9 = v55 + v52;
		v7 = __ROL4__(v9 ^ v53, 8);
		v17 = v7 + v54;
		v69 = __ROL4__(v17 ^ v55, 7);
		v56 = v47 + v37;
		v57 = __ROL4__(v56 ^ v30, 16);
		v58 = v57 + v68;
		v59 = __ROL4__((v57 + v68) ^ v47, 12);
		v13 = v59 + v56;
		v11 = __ROL4__(v13 ^ v57, 8);
		v6 = v11 + v58;
		v16 = __ROL4__(v6 ^ v59, 7);
		v60 = v71 + v44;
		v61 = __ROL4__(v60 ^ v38, 16);
		v62 = v61 + v31;
		v63 = __ROL4__(v62 ^ v71, 12);
		v70 = v63 + v60;
		v14 = __ROL4__((v63 + v60) ^ v61, 8);
		v12 = v62 + v14;
		v5 = __ROL4__((v62 + v14) ^ v63, 7);
		--v75;
	}
	while ( v75 != 0 );
   ```
   -> rotate 的數字為 16, 12, 8, 7
   -> ChaCha20
2. Variant / Nonce
   Original ChaCha20 →  64-bit counter → 可跑約 $2^{64}$ blocks
   IETF ChaCha20        →  32-bit counter → 可跑約 $2^{32}$ blocks
   XChaCha20              →  會有額外的 HChaCha / 192-bit nonce 處理
   No nonce                 →  不符合標準 ChaCha20 state 用法
   程式碼中
   ```c
   v74 = a2[1];
    v73 = strlen(s: v74);
    result = 2;
    if ( v73 <= 4000000000h ) {
	    ...
   ```
   長度 <= `4000000000` = $2^{38}$ bytes
   又
	1. 從 `v65 = v72 & 0x3F;` 得知：`v72` mod 64（0x3F = 63）-> 每 64 bytes 會進一次區塊，重新產生一批 keystream
	2. 從 `_BYTE v85[64]` -> 64-byte keystream block
	-> 64-byte / block
	
	綜合上述：
	--> $2^{38} / 64 = 2^{32}$ blocks ->  IETF / RFC 8439
   
1. `qmemcpy(v78, "expand 32-byte k", sizeof(v78));` -> 32-byte = 256-bit key
2. flag = `a2-b2-c4`

---

# sample-03

## 題目

Analyze `sample03` and select one option from each group.

| A: Algorithm                                                                                  | B:  Variant                                                                                                                           |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| - A1: CRC-16                               <br>- A2: CRC-32<br>- A3: CRC-64<br>- A4: Adler-32 | - B1: ISO-HDLC                                                   <br>- B2: ISCSI / CRC32C / Castagnoli<br>- B3: MPEG-2<br>- B4: BZIP2 |

| C: Init / Reflection                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| - C1: All ones; RefIn = true, RefOut = true                          <br>- C2: All zeros; RefIn = false, RefOut = false<br>- C3: All ones; RefIn = false, RefOut = false<br>- C4: All zeros; RefIn = true, RefOut = true |

## 解題
