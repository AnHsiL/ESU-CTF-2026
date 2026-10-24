#Reverse

## 題目

**idb - unreachable**
To download attachment, refer to challenge idb - corrupted main

使用跟 [[idb - corrupted main]]  一樣的檔案 `lab01.i64`

## 解題
1. 題目為 unreachable -> 有 `main` 無法到達的程式
2. 用 IDA 打開 `lab01.i64`，找到標記紅色（IDA 不視為 main 可達的執行路徑）的區域
   看到明顯的 function 開頭+結尾
   ```armasm
   endbr64
   push    rbp
   ...
   leave
   retn
   ```
   選取按 `p`(Create function)
3. 從 `F5` 的 pseudo code 可以發現
   ```c
   unsigned __int64 sub_1189()
	{
		int i; // [rsp+Ch] [rbp-34h]
		_QWORD s[5]; // [rsp+10h] [rbp-30h] BYREF
		unsigned __int64 v3; // [rsp+38h] [rbp-8h]
		
		v3 = __readfsqword(0x28u);
		s[0] = 0x5A5B474874727F75LL;
		qmemcpy(&s[1], "@lUF]PGZ\\]lZ@lF]AVRP[RQ_VN", 26);
		for ( i = 0; i <= 33; ++i )
		*((_BYTE *)s + i) ^= 0x33u;
		puts((const char *)s);
		return v3 - __readfsqword(0x28u);
	}
   ```
   `sub_1189()` ：
   1. 把 `0x5A5B474874727F75LL` 寫進 x86-64 little-endian 記憶體（8 bytes）
   2. 在後面的記憶體中放 `@lUF]PGZ\\]lZ@lF]AVRP[RQ_VN`（26 bytes）
   3. 兩者的組合後（34 bytes） XOR `0x33`
4. 反運算 `decode0x33.py`
   ```python
   data = (
	    (0x5A5B474874727F75).to_bytes(8, "little")
	    + b"@lUF]PGZ\\]lZ@lF]AVRP[RQ_VN"
	)
	decoded = bytes(x ^ 0x33 for x in data)
	print(decoded)
   ```
5. flag = `FLAG{this_function_is_unreachable}`
