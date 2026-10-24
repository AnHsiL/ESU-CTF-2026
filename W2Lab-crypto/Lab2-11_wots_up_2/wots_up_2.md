#Crypto 

## 題目

**wots_up_2**  
This was an old challenge forwarded from ECSC 2023
I think WOTS Scheme is cool lol XD

並提供了 `data.json` 及 source code，簡化後：

```python
w = Winternitz()
output = {
	"signatures": []
}

for i in range(20):
	message = f"{w.pub_key[0].hex()} sent {int.from_bytes(urandom(1), "big")} WOTScoins to {urandom(32).hex()}".encode()
	signature = w.sign(message)
	assert w.verify(signature, message)
	output["signatures"].append({
		"message": message.decode(),
		"signature": [s.hex() for s in signature],
	})

message2 = f"{w.pub_key[0].hex()} sent 999999 WOTScoins to me".encode()
signature2 = w.sign(message2)
assert w.verify(signature2, message2)

with open("flag.txt") as f:
	flag = f.read().strip().encode()

aes_key = bytes([s[0] for s in signature2])
aes_iv = urandom(16)
cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
encrypted = cipher.encrypt(flag)

with open("data.json", "w") as f:
	output["public_key"] = [s.hex() for s in w.pub_key]
	output["iv"] = aes_iv.hex()
	output["enc"] = encrypted.hex()

	f.write(json.dumps(output))

```

### Winternitz One-Time Signature（WOTS）
只能使用一次的 PQC 數位簽章方法，能夠顯著減少簽章和公鑰的大小[^1]
##### 運作原理
`pr[]`：私鑰
`pub[]`：公鑰

1. **產生金鑰**：隨機產生一串私鑰，對私鑰進行多次重複雜湊，形成「雜湊鏈」作為公鑰。
2. **簽章**：根據要傳送的訊息內容，決定每一段資料需要執行多少次雜湊運算來產生簽章。
3. **驗證**：接收方把收到的簽章繼續做對應次數的雜湊，看最後結果是否與公鑰相符。
```
	pr[i]      |       pr[0]             pr[1]             pr[2]          ...
	-----------|----------------------------------------------------------------
	  ↓ hash   |         ↓ hash            ↓ hash            ↓ hash
	 x1        |
	  ↓ hash   |         ↓ hash            ↓ hash            ↓ hash
	 x2        |                   x(255-pr[1])=pub[1]
	  ↓        |         ↓ hash                              ↓ hash
	 ...       |        ... 
	  ↓        |  x(255-pr[0])=pub[0]                        ↓ hash
x256 = pub[0]  |                                     x(255-pr[2])=pub[2] 
```
**範例：**
假設某位置
```
data_hash[i] = 100
```
簽章：hash 多次
$$
\texttt{sig[i]} = \texttt{hash}^{255 - 100}(\texttt{pr[i]}) = \texttt{hash}^{155}(\texttt{pr[i]})
$$
驗證：再 hash `100 + 1 = 101` 次，剛好達到 hash `256` 次 = `pub[i]`
##### 私鑰重複使用 洩漏
假設
- 已知某簽章位置 $i$ `hash byte = 200` -> 在位置 $i$ 的已知簽章為 $\texttt{hash}^{55}(\texttt{pr[i]})$
- 目標訊息在位置 $i$ 的簽章需要 $\texttt{hash}^{105}(\texttt{pr[i]})$
獲得目標簽章：
- 已知簽章再 hash `105 - 55 = 50` 次 = 目標簽章

---

## 解題
1. 觀察 source code，題目的流程：
	1. 建立一個 Winternitz 簽章物件，並使用同一把 WOTS key 簽 20 次 --> 可以利用
	   ```python
	   w = Winternitz()
	   for i in range(20):
	        message = ...
	        signature = w.sign(message)
	        output["signatures"].append({
	            "message": message.decode(),
	            "signature": [s.hex() for s in signature],
	        })
	   ```
	   message 的內容為交易訊息，包含三部分：
	   ```
	   sender                    amount        receiver
w.pub_key[0].hex()        0~255         random 32 bytes
	   ```
	   其中 `amount` = `int.from_bytes(urandom(1), "big")`為 1 byte 隨機值 -> 0~255
	2. 簽署一個特殊訊息，不放入 `data.json`
	   ```python
	   message2 = f"{w.pub_key[0].hex()} sent 999999 WOTScoins to me".encode()
	   ```
	   - 特殊訊息長相範例
		   ```text
		   signature2 = [
				s0 = [A1 35 F2 ...],
				s1 = [7C BB 90 ...],
				s2 = [43 D1 00 ...],
				...
			]
		   ```
	   
	   並用特殊訊息簽章的**第一個 byte** 建立 CBC mode AES key 來加密 flag
	   ```python
	   aes_key = bytes([s[0] for s in signature2])
		cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
		encrypted = cipher.encrypt(flag)
	   ```
	1. 把攻擊者可以看到的東西寫入 `data.json`
	   ```json
	   {
		    "signatures": [
		        {
		            "message": "... sent 12 WOTScoins to ...",
		            "signature": [
		                "...",
		            ]
		        },
		        ...
		    ],
		    "public_key": [
		        "...",
		    ],
		    "iv": "...",
		    "enc": "..."
	}
	   ```
	2. 整體流程
	   ```
					Winternitz private key
	          ┌──────────────┴───────────────┐
	     20 random messages             target message
	       M1 ... M20                 M* = "...999999..."
	          ▼                              ▼
	     WOTS signatures                 signature2
	     σ1 ... σ20                         σ*
	          │ PUBLIC                       │ SECRET
	          ▼                              ▼
	      data.json                  take first byte
	                                 of each element
	                                       ▼
	                                   AES key
	                              ┌────────┴────────┐
	                             flag              IV
	                              └──── AES-CBC ────┘
	                                       ▼
	                                      enc
	                                       ▼
	                                   data.json
	   ```
2. 寫腳本，利用 WOTS 重複簽章的缺口
   - `j` = 第幾組訊息
	- `i` = SHA256 的第幾個 byte / 第幾條 hash chain
   ```python
	target_msg = (f"{public_key[0].hex()} sent 999999 WOTScoins to me").encode()
	target_hash = hashlib.sha256(target_msg).digest()
	target_signature = []
	
	for i in range(32):
	    h = target_hash[i]
	    for j in range(len(hashes)):
	        known = hashes[j][i]
	
	        if known >= h:
	            sig = signatures[j][i]
	            for _ in range(known - h):   # hash() (known - h) 次
	                sig = hashlib.sha256(sig).digest()
	            target_signature.append(sig)
	            break
	
	aes_key = bytes([s[0] for s in target_signature])
	cipher = AES.new(aes_key, AES.MODE_CBC, iv)
	flag = cipher.decrypt(enc)
	
	print(flag)
   ```
1. flag = `ECSC{0ne_m0r3_t1m3_s1gn4tur3_ff}`

[^1]: [密碼學 - 一次性簽章](https://codingman.cc/one-time-signature/#Winternitz-One-Time-Signature-Winternitz-%E7%B0%BD%E7%AB%A0)
