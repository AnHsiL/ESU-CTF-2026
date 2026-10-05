#Crypto

## 題目

**observer**  
I love observing 🐿️ Can u leak the flag plz ... for me ...

`nc 45.77.20.255 31011`
並提供了 source code，簡化後：

```python
print(flag.decode()[:7], len(flag))

def xor(a, b):
        return bytes(x ^ y for x, y in zip(a, b))

while True:
    msg = input("> ")
    msg = bytes.fromhex(msg)
    msg = msg.ljust(len(flag))
    print('<', md5(xor(msg, cycle(flag))).hexdigest())
```

### MD5
一種按照 block 處理的訊息摘要演算法（MD5 Message-Digest Algorithm），產生一個128位元的雜湊值，用於確保訊息傳輸完整一致 [^1][^2]
##### 步驟
>MD5 block 長度為 512 bit = 64 bytes

![[W2-15_MD5.png|center]]
1. 將訊息加上 Padding，使得 
   $$\texttt{訊息長度 mod}\, 512 = 448 = 3 \times 128 \texttt{ bits}$$

2. 加上 64 bits = 8 bytes 訊息長度，如果長度超過 $2^{64}$ 個位元，則只取最低 64 位元的資料
3. 以每 512 bits  = 64 bytes 為單位，將訊息分割為 `L` 個區塊 $P_0, P_1, ..., P_{L-1}$
4. hash

   >[!abstract] Padding in MD5
   >MD5 的長度資訊 Padding 規則是：
   >1. 先補一個 1 bit 再補足夠的 0 bits（起始 byte= 100...0）
   >2. 最後補上 8 bytes，記錄原始資料的 bit 長度。
   >   ```
   >   長度資訊：
80 b8 01 00 00 00 00 00 00
│  └───────────────┬──────┘
│          440 bits = 0x1b8
│              (8 bytes)
│
└─ 10000000（二進位）
   1 bit + 7 個 0 bits
   >   ```
   >   --> 原始資料長度可能為 `% 64` 後為 `64 - 1 - 長度資訊(8)  = 55 bytes` 的值


---

## 解題

1. 觀察 source code，發現
   - 題目提供 flag 長度 `LEN` 和 flag 前 7 bytes
     ```python
     print(flag.decode()[:7], len(flag))
     ```
	- 可以控制 `msg`，並且每次送出值都回傳 `md5(xor(msg, cycle(flag)))` 
		- `H = MD5(msg XOR cycle(flag))` -> 可預測 Length Extension 後的 Hash
	  - `cycle(flag)`：超過 flag 長度時，會從頭重複使用
	    ```python
	    flag = ABCDEFGHIJK
	cycle(flag) = ABCDEFGHIJKABCDEFGHIJK...
	    ```

	-> <mark style="background: #FFF3A3A6;">MD5 Length Extension</mark>
1. 送全 '0' 給 server，利用 xor 0 的特性得到 `H = MD5(flag)[:msg_len]`
2. 流程
	```
	送給 Server：
	[  00 00 00 ... ][ padding XOR flag ]        <- 猜 flag
	        ▼                 ▼
	    XOR flag          XOR flag
	        ▼                 ▼
	[       M       ][      padding     ]
				   ▼
				  MD5
				   ▼
		和 Length Extension 預測比較
	```
		
3. 當改變 `msg_len` 時，padding 會跟著改，可以用來猜測不同的位置，[[#`msg_len` 與 padding 猜測關係|範例]]
   -> 每次找合適的 `msg_len`
   ```python
   best = None    
   for k in range(flag_len + 1):
        msg_len = (BLOCK_LEN - PAD_LEN) + BLOCK_LEN*k
        if msg_len < flag_len:
            continue

        positions = [(msg_len + i) % flag_len for i in range(PAD_LEN)]
        to_guess = sorted({pos for pos in positions if flag[pos] is None})

        if not to_guess:
            continue

        if best is None or len(to_guess) < len(best[1]):
            best = (msg_len, to_guess)

    if best is None:
        raise RuntimeError("找不到可用的 padding 位置")

    msg_len, to_guess = best
    if len(to_guess) > 2:
        raise RuntimeError("需同時猜過多 bytes")
   ```
4. Length Extension
   ```python   
	msg = b"\x00" * msg_len
	md5 = oracle(msg)
	new_MD5 = HashTools.new("md5")
	new_msg, sign = new_MD5.extension(
        secret_length=0,
        original_data=msg,
        append_data=b"",
        signature=md5
    )
    padding = new_msg[msg_len:]
   ```
5. 打包送出 msg，並將 server 回傳的值和 Length Extension 的預測比較
    ```python
	found = False
    for guess in product(CHARSET, repeat=len(to_guess)):
        guess_map = dict(zip(to_guess, guess))

        xor_pad = bytes(
            padding[i] ^ (
                flag[(msg_len + i) % flag_len]
                if flag[(msg_len + i) % flag_len] is not None
                else guess_map[(msg_len + i) % flag_len]
            )
            for i in range(len(padding))
        )

        if oracle(msg + xor_pad) == sign:
            for pos, value in guess_map.items():
                flag[pos] = value

            print(bytes(c if c is not None else ord("-") for c in flag).decode())
            found = True
            break

    if not found:
        raise RuntimeError("找不到匹配值")
    ```
    其中 `guess map` = 
    ```
    {
	    未知位置1: 猜測字元1,
	    未知位置2: 猜測字元2
	}
    ```
6. 最後 `while None in flag:` 持續破解
   ![[W2-15_flag.png|525]]
7. flag = `FLAG{a2ea3f511025f4d1258c7407542af4dfea4af68d8ca4829f792eb17737329bbc}`


---
##### `msg_len` 與 padding 猜測關係
舉例：
假設 FLAG = 'ABCDEFGWXYZ1234'，長度 15
```
FLAG 索引：0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
已知：     A B C D E F G ? ? ?  ?  ?  ?  ?  ?
```
當 `msg_len = 55`（55 % 15 = 10）
```
索引： 10 11 12 13 14 0 1 2 3
已知：  ?  ?  ?  ?  ? A B C D
	   ↑  ↑  ↑  ↑  ↑
		   猜這裡
```
一次猜 5 個字元，組合的數量太多了 -> 放棄從 `msg_len = 55` 開始
當 `msg_len = 119`（119 % 15 = 14）
```
索引： 14 0 1 2 3 4 5 6 7
已知：  ? A B C D E F G ?
	   ↑               ↑ 
			 猜這裡
```
當 `msg_len = 375`（375 % 15 = 0）
```
索引： 0 1 2 3 4 5 6 7 8
已知： A B C D E F G W ?
					  ↑
					猜這裡
```   
當 `msg_len = 631`（631 % 15 = 1）
```
索引： 1 2 3 4 5 6 7 8 9
已知： B C D E F G W X ?
					  ↑
					猜這裡
```
當 `msg_len = 887`（887 % 15 = 2）
```
索引： 2 3 4 5 6 7 8 9 10
已知： C D E F G W X Y  ?
					   ↑
					 猜這裡
```

[^1]: [一文读懂MD5](https://zhuanlan.zhihu.com/p/402362868)
[^2]: [4-3 MD5 訊息摘要](https://www.tsnien.idv.tw/Security_WebBook/chap4/4-3%20MD5%20%E8%A8%8A%E6%81%AF%E6%91%98%E8%A6%81.html)
