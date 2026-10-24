#Crypto 

## 題目

**none_unique**  
None Unique, have u saw the advertisement (I forgot which ads actually XDDD)

`nc 45.77.20.255 31012`

並提供了 source code，簡化後：

```python
print("U have 1 min, gogo!")

for i in range(20):
    key = os.urandom(16)
    print(key.hex())
    msg1 = input('1> ')
    msg1 = bytes.fromhex(msg1)
    msg2 = input('2> ')
    msg2 = bytes.fromhex(msg2)
    if key in msg1 and key in msg2 and msg1!=msg2 and md5(msg1).hexdigest() == md5(msg2).hexdigest():
        print('AC')
    else:
        print('WA')
        exit()

print(flag.decode())
```

### Fastcoll 工具
[fastcoll](https://github.com/brimstone/fastcoll) 是 MD5 Collision Generator，可以針對一個共同 prefix，產生：
```
prefix + collision_block_A
prefix + collision_block_B
```
兩者內容不同但 MD5 相同

---

## 解題

1. 觀察 source code，發現題目的要求輸入 `msg1`、`msg2`：
   - `key` in `msg1`
   - `key` in `msg2`
   - `msg1` != `msg2`
   - `md5(msg1)` == `md5(msg2)`
1. MD5 碰撞 -> 使用 fastcoll 工具
   - 安裝
	   ```bash
	   sudo apt update
		sudo apt install -y git g++ libboost-all-dev
		
		git clone https://github.com/brimstone/fastcoll.git
		cd fastcoll
		
		g++ -O3 *.cpp   -DBOOST_TIMER_ENABLE_DEPRECATED   -lboost_filesystem   -lboost_program_options   -lboost_system   -o fastcoll
		./fastcoll
	   ```
	- 使用測試：在 prefix 寫入 "test123"，並將內容不同但 MD5 相同的兩個值分別寫進 `mdg1`、`msg2`
	  ```bash
	  echo -n "test123" > prefix.bin
	./fastcoll -p prefix.bin -o msg1.bin msg2.bin
	  ```
	  兩個的 MD5 相同：`md5sum msg1.bin msg2.bin`
	  但內容不同：`cmp msg1.bin msg2.bin`
1. 在 python 腳本中呼叫
   ```python
   # 在 WSL 的 "home/[user]/ctf/" 中安裝
   FASTCOLL_DIR = Path( r"\\wsl.localhost\Ubuntu-24.04\home\[user]\ctf\fastcoll")
	WSL_DIR = "/home/[user]/ctf/fastcoll" # 在 WSL 呼叫時用的路徑
	
	prefix = FASTCOLL_DIR / "prefix.bin"
	msg1 = FASTCOLL_DIR / "msg1.bin"
	msg2 = FASTCOLL_DIR / "msg2.bin"
	
	prefix.write_bytes([prefi])
    subprocess.run([
        "wsl", "-d", "Ubuntu-24.04",
        f"{WSL_DIR}/fastcoll",
        "-p", f"{WSL_DIR}/prefix.bin",
        "-o",
	        f"{WSL_DIR}/msg1.bin",
	        f"{WSL_DIR}/msg2.bin",
    ], check=True)

    m1 = msg1.read_bytes()
    m2 = msg2.read_bytes()
   ```
2. 完整流程：
   ```python
   for i in range(20):
		key = bytes.fromhex(r.recvline().decode())
		prefix.write_bytes(key)
		
		# 呼叫生成 MD5 collision 的 msgs
		# ...
		# ...
		
		r.recvuntil(b"1> ")
	    r.sendline(m1.hex().encode())
	
	    r.recvuntil(b"2> ")
	    r.sendline(m2.hex().encode())
	    r.recvline() # AC / WA

	print(r.recvline())
   ```
3. flag = `FLAG{cace491a169af193d75ef6bdb6d8de3422f914e8ead7c0d8217b8a291cdec39b}`
