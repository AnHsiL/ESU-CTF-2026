#Crypto 

## 題目

**merkle_trees**  
Challenge forwarded from CryptoHack
Merkle tree is important in modern fintech XD

並提供了 `output.txt` 及 source code，簡化後：

```python
def hash256(data):
    return sha256(data).digest()

def merge_nodes(a, b):
    return hash256(a+b)

def gen_test(is_true):
    a = hash256(os.urandom(8))
    b = hash256(os.urandom(8))
    c = hash256(os.urandom(8))
    d = hash256(os.urandom(8))
    bias = b"" if is_true else os.urandom(8)
    left = merge_nodes(a, b+bias)
    right = merge_nodes(c, d)
    root = merge_nodes(left, right)
    return a.hex(), b.hex(), c.hex(), d.hex(), root.hex()

challenges = []
for bit in bin(int(FLAG.hex(),16))[2:]:
    a, b, c, d, root = gen_test(int(bit))
    challenges.append([a, b, c, d, root])

with open("output.txt", "w") as f:
    for chal in challenges:
        f.write(str(chal))
        f.write("\n")
```

---

## 解題
1. 觀察 source code，發現是簡單的 merkle tree
   - 題目先將 `flag` 轉為二進制，每次輸入一個 bit 給 `gen_test()`
   - `gen_test()` 判斷 `bit`，如果`bit`是
	   - `1` -> 不加 bias 到 `b`
	   - `0` -> 加 bias 到 `b`
	    
	   接著合併成 merkle tree
   - `output.txt` 每筆包含 `a`, `b`, `c`, `d`, `root` 五個資料
1. 重現整個 merkle tree 流程，flag 的每一個 bit 用 0 和 1 猜測，如果新結果和 `root` 一樣 -> 沒有 bias -> 當 bit = 1，不一樣則為 0
2. 寫腳本
   ```python
   import os
	import ast
	from hashlib import sha256
	
	def hash256(data):
	    return sha256(data).digest()
	
	def merge_nodes(a, b):
	    return hash256(a+b)
	
	CUR_DIR = os.path.dirname(os.path.abspath(__file__))
	OUT_DIR = os.path.join(CUR_DIR, "output.txt")
	
	flag = b''
	with open (OUT_DIR, "r") as f:
	    for line in f:
	        line = line.strip()
	        chal = ast.literal_eval(line)
	        a = bytes.fromhex(chal[0])
	        b = bytes.fromhex(chal[1])
	        c = bytes.fromhex(chal[2])
	        d = bytes.fromhex(chal[3])
	        r = bytes.fromhex(chal[4])
	
	        left = merge_nodes(a, b)
	        right = merge_nodes(c, d)
	        root = merge_nodes(left, right)

	        flag = flag + b'1' if r == root else flag + b'0'
	
	print(int(flag, 2).to_bytes((len(flag)+7)//8, 'big'))
   ```
3. flag = `FLAG{now_u_can_learn_how_blockchain_works!}`
