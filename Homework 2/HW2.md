學號：`415551013`
姓名：呂安曦
## 通訊架構與要求
```
	Alice <----------> Bob
```
- 通訊參與者：Alice、Bob
- 通訊規則：雙方選擇 `True` 才完成訊息傳遞
   *選擇 `False`仍然會傳送資料，避免第三方推測出選擇*
- 加密要求：
	- `True` / `False` 的選擇：第三方、選 `False` 的人不能知道他人選擇
	- 機密性：第三方不能解讀訊息內容

> **目標**：讓 Alice 和 Bob 在不暴露各自選擇下，只有雙方都同意時完成安全通訊

預期結果：

| Alice   | Bob     | Alice 得到   | Bob 得到     |
| ------- | ------- | ---------- | ---------- |
| `True`  | `True`  | Bob 的訊息    | Alice 的訊息  |
| `True`  | `False` | Bob 拒絕     | 無對方選擇或訊息資訊 |
| `False` | `True`  | 無對方選擇或訊息資訊 | Alice 拒絕   |
| `False` | `False` | 無對方選擇或訊息資訊 | 無對方選擇或訊息資訊 |

---
## 演算法設計
##### 系統模型
- 通訊架構：Alice <---> Bob 
- 安全假設：參與者皆為 curious-but-honest、僅考慮訊息和選擇的機密性

##### 參數設定

| 參數             | 說明                                          |
| -------------- | ------------------------------------------- |
| $G,q,g$        | 公開群參數：$G$ 為 DDH 假設成立的質數階循環群，階為 $q$，生成元為 $g$ |
| $P$            | 加密公開的大質數模數                                  |
| $L$            | 公開約定的訊息容量上限 (bytes)                         |
| $w$            | 長度欄位位元數，$w=\lceil\log_2(L+1)\rceil$         |
| $N$            | 加密明文總位元數，$N=1+w+8L$                         |
| $pk_B=(h,u,v)$ | Bob 傳給 Alice 的公鑰                            |
| $sk_B=b$       | Bob 選 True 時保留的解密私鑰                         |
- $P$ 選用 RFC 3526 §3 Group 14 定義的 2048-bit 安全質數，滿足 $P=2Q+1$
- $Q = (P - 1) / 2$，是使用的子群元素數量
- $g$ = 2，階恰為 $q$，因此其冪次可產生整個子群：$G=\{g^x\bmod P\mid x\in\mathbb Z_q\}$
##### 協定
協定參考 Bellare et al. 的 DDH 型 lossy encryption [^1] 設計，以單向 (Alice -> Bob) 說明，反向為相同流程
- Alice 的輸入：Choice_A、msg_A
- Bob   的輸入：Choice_B

![[HW2_protocol.png|center|578]]

**函式設計**
1. Generate normal key
   ```
   NormalKeyGen():
		a ← RandomZq()
		b ← RandomZq()
		h ← Pow(g, a)
		u ← Pow(g, b)
		v ← Pow(g, (a × b) mod q)
		pk ← (h, u, v)
		sk ← b
		Return (pk, sk)
   ```
2. Generate lossy key
   ```
   LossyKeyGen():
		a ← RandomZq()
		b ← RandomZq()
		While c = (a × b) mod q, do
			c ← RandomZq()
		h ← Pow(g, a)
		u ← Pow(g, b)
		v ← Pow(g, c)
		pk ← (h, u, v)
		Return pk
   ```
3. Pack and Unpack message
   將選擇 (0/1) 及容量至於訊息前方，並用 padding 補足訊息長度，避免攻擊者透過訊息長度推測資訊
   ```
   Pack(choice, msg, L):
		w ← ceil(log2(L + 1))
		If choice = True:
			length ← ByteLength(msg)
			Require length ≤ L
			body ← msg || RandomBytes(L - length)
			Return 1 || UIntToBits(length, w) || BytesToBits(body)
		Else:
			body ← RandomBytes(L)
			Return 0 || UIntToBits(0, w) || BytesToBits(body)
	
	Unpack(P, L):
		Require BitLength(P) = 1 + w + 8L
		flag   ← first bit of P
		length ← BitsToUInt(next w bits)
		body   ← BitsToBytes(remaining 8L bits)
		If flag = 0:
			Return REJECT
		If length > L:
			Return ERROR
		Return (ACCEPT, first length bytes of body)
   ```
4. Encrypt
   ```
   EncryptBit(pk, d):
		Require d ∈ {0,1}
		(h, u, v) ← pk
		r ← RandomZq()
		s ← RandomZq()
		X ← Mul(Pow(g, r), Pow(h, s))
		Y ← Mul(Pow(g, d), Mul(Pow(u, r), Pow(v, s)))
		Return (X, Y)
		
	EncryptBits(pk, P):
		C ← empty list
		For each bit d in P, in order:
			Append EncryptBit(pk, d) to C
		Return C
   ```
5. Decrypt
   ```
   DecryptBit(sk, pair):
		b ← sk
		(X, Y) ← pair
		Z ← Mul(Y, Inv(Pow(X, b)))
		If Z = 1_G:
			Return 0
		If Z = g:
			Return 1
		Return ERROR
	
	DecryptBits(sk, C):
		Require C contains exactly N pairs
		P ← empty bit string
		For each pair in C, in order:
			d ← DecryptBit(sk, pair)
			If d = ERROR:
				Return ERROR
			Append d to P
    Return P
   ```


---

## 簡易安全性分析
協定安全性參考 Bellare et al. 的 DDH 型 lossy encryption [^1]

1. **接收者 (Bob) 的選擇隱私**  
    正常公鑰與 lossy 公鑰計算上不可區分，因此將 Bob 的 `True`／`False` 分別對應至這兩種公鑰，可以隱藏 Bob 的選擇。
    
2. **訊息機密性與拒絕者隱私**  
    - Alice=`True` 時加密 `1 || 訊息長度 || 訊息與填充`
    - Alice=`False` 時加密 `0 || 0 || 亂數填充`。
    只有雙方皆為 `True`，Bob 才能取得訊息，Bob=`False` 時，即使分析全部收到的密文，也無法得知 Alice 的選擇或訊息。
    其中 Bob 的正常模式保護訊息不被第三方解讀、lossy 模式使密文分布與明文無關。
    
3. **訊息長度隱私**  
    協定選擇使用固定容量、相同封包數量與長度，避免第三方直接由資料大小推測雙方的選擇。
    **限制**：容量須事先約定，不能依選擇或實際訊息長度調整。
    
4. **安全範圍**  
    協定適用於 Curious-but-honest、端點秘密不外洩的情境。  


---

# 實驗
所有實驗皆為三次取平均
#### capacity 對執行時間的影響
![[capacity_total.png|center|506]]
可以看到，capacity 與執行時間呈現行增長，capacity 越大，隱私保護協定所需時間越長
#### 固定 capacity 下實際訊息長度的公鑰、密文大小
實驗設定公鑰為 768 bytes
![[capacity_length.png]]
可以看到相同 capacity 下，TT／TF／FT／FF 的公鑰與密文長度完全一致
-> 無法單從資料長度判斷雙方的選擇。
密文隨 capacity 增加而變大，因為訊息會補齊容量後再逐位元加密。


[^1]: [Bellare, M., & Yilek, S. (2009). Encryption schemes secure under selective opening attack. _Cryptology ePrint Archive_.](https://cseweb.ucsd.edu/~syilek/BY-ec09full.pdf)
