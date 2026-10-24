#Crypto

## 題目

**why_line**  
I just want to meet you again <3

`nc 45.77.20.255 31010`
並提供了 source code，簡化後：

```python
salt = os.urandom(16)
while True:
    cmd = input("CMD > ")
    if cmd == 'SIGN':
        content = input("MSG > ")
        content = bytes.fromhex(content)
        if b'meet me next wednesday' not in content:
            print(md5(salt + content).hexdigest())
        else:
            print("ERROR, BAD HACKER")
    
    elif cmd == 'SEND':
        content = input("MSG > ")
        content = bytes.fromhex(content)
        signature = input("SIG > ")
        if signature == md5(salt + content).hexdigest():
            print("GOOD, I've READ IT")
            if b'meet me next wednesday' in content:
                print(flag.decode())
        else:
            print("SORRY ... I can't believe u")
```

---

## 解題

1. 觀察 source code，發現
   - 伺服器有兩個功能："MD5 簽署"、"驗證"，並且不能拿要驗證的句子簽章
   - 有加 salt，但所有的 salt 是同一個
    
	--> MD5 padding attack
	```python
	if MD5(A) = MD5(B)
	->  MD5(A+x) = MD5(B+x)
	```
1. 利用 length-extension-tool `Hashtools` 延伸原有的 hash 值，偽造新的簽章
2. 寫腳本
    ```python
	r = remote(HOST, PORT)
	
	target = b'meet me next wednesday'
	payload = b'A' *16
	
	r.sendlineafter(b"CMD > ", b"SIGN")
	r.sendlineafter(b"MSG > ", payload.hex().encode())
	
	rec_sign = r.recvline().decode().strip()

	new_MD5 = HashTools.new("md5")
	msg, sign = new_MD5.extension(
	    secret_length=16,       # salt 長度
	    original_data=payload,
	    append_data=target,
	    signature=rec_sign
	)
	
	r.sendlineafter(b"CMD > ", b"SEND")
	r.sendlineafter(b"MSG > ", msg.hex().encode())
	
	r.sendlineafter(b"SIG > ", sign.encode())
	r.recvline()  # GOOD, I've READ IT
	print(r.recvline().decode())
    ```
3. flag = `FLAG{f0085dcd103ebd954ce45a30fe9f8f86cb61a37a38c60fc5b8ef22d8d87c915a}`