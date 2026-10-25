#Reverse 


| 選項              | 常見辨識特徵                           |
| --------------- | -------------------------------- |
| **A1 CRC-16**   | 16-bit state / polynomial        |
| **A2 CRC-32**   | 32-bit state，常輸出 8 個 hex digit   |
| **A3 CRC-64**   | 64-bit state                     |
| **A4 Adler-32** | 主要是兩個累加和，不會有逐 bit polynomial XOR |

| 選項                         | Polynomial / 特徵                                                                 | Reflection          |
| -------------------------- | ------------------------------------------------------------------------------- | ------------------- |
| **B1 ISO-HDLC**            | `0x04C11DB7`；<br>反射形式常看到 `0xEDB88320`                                           | RefIn/RefOut = true |
| **B2 CRC32C / Castagnoli** | `0x1EDC6F41`；                                          <br>反射形式常看到 `0x82F63B78` | true                |
| **B3 MPEG-2**              | `0x04C11DB7`                                                                    | false               |
| **B4 BZIP2**               | `0x04C11DB7`                                                                    | false               |
> [!abstract] 反射形式：
> 把 bit 的處理方向反過來，從最低位 LSB 開始算，而不是從最高位 MSB 開始算
> ```
> 非反射 CRC                     反射 CRC
> ------------------            ------------------
> 看最高 bit (MSB)              看最低 bit (LSB)
> 左移 <<                       右移 >>
> poly = 0x04C11DB7             poly = 0xEDB88320
> ```
> 
> e.g.
> - 原本：`11010010`
> - bit reflection：`01001011`

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
1. 從程式碼看到，
   ```c
	__int64 __fastcall main(int a1, char **a2, char **a3)
	{
		char *v3; // rcx
		unsigned __int8 v4; // al
		char *v5; // rcx
		unsigned int i; // esi
		int j; // eax
		
		if ( a1 == 2 ) {
			v3 = a2[1];
			v4 = *v3;
			v5 = v3 + 1;
			for ( i = -1; v4 != 0; v4 = *(v5 - 1) ) {
				  i ^= v4;
				  for ( j = 8; j != 0; --j )
					i = (i >> 1) ^ ((i & 1) != 0 ? 0xEDB88320 : 0);
				  ++v5;
				}
				printf(format: "%08x\n", ~i);
				return ferror(stream: stdout) != 0;
		}
		else {
			fprintf(stream: stderr, format: "usage: %s text\n", *a2);
			return 2;
		}
	}
   ```
   `ESI` 一直進行逐位 XOR 更新，`unsigned int i; // esi` -> `i` 在 `ESI`
	1. `for ( i = -1; v4 != 0; v4 = *(v5 - 1) )` -> ESI 初始值為 -1     
	   -> 檢查 asm 程式查看使用的 bits 數
	2. 發現為 4-byte = 32-bit
	   ```
	   1198                 mov     esi, 0FFFFFFFFh
	   ```
	-> CRC-32
2. 程式中出現 `0xEDB88320` -> ISO-HDLC
3. 承上 Reflection = true，init = `0xFFFFFFFF` =  all ones
4. flag = `a2-b1-c1`


---
# sample-04

## 題目

Analyze `sample04` and select one option from each group.

| A: Algorithm                                                                                  | B:  Variant                                                                                                                           |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| - A1: CRC-16                               <br>- A2: CRC-32<br>- A3: CRC-64<br>- A4: Adler-32 | - B1: ISO-HDLC                                                   <br>- B2: ISCSI / CRC32C / Castagnoli<br>- B3: MPEG-2<br>- B4: BZIP2 |

| C: Init / Reflection                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| - C1: All ones; RefIn = true, RefOut = true                          <br>- C2: All zeros; RefIn = false, RefOut = false<br>- C3: All ones; RefIn = false, RefOut = false<br>- C4: All zeros; RefIn = true, RefOut = true |

## 解題
1. 觀察 main
   ```c
   i = (i >> 1) ^ ((i & 1) != 0 ? 0x82F63B78 : 0);
   ```
   - `i` 初始值 `0FFFFFFFFh` -> 32-bits、all-ones
   - 逐 bit XOR、`0x82F63B78` -> B2. CRC32C / Castagnoli
   - `>>` -> reflection
1. flag = `a2-b2-c1`