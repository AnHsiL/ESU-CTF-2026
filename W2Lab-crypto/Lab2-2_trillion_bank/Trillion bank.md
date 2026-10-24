#Crypto

## 題目

**trillion_bank**
If you can hack The Great Trillion Bank, please contact trilliongame21@gmail.com
`nc 45.77.20.255 31001`

並提供了 source code，簡化後：
```python
key = os.urandom(16)
aes = AES.new(key, AES.MODE_ECB)

def pad(data):
    return data + bytes([-len(data)%16]*(-len(data)%16))

def unpad(data):
    padlen = int(data[-1])
    if padlen <= 15 and bytes([data[-1]])*padlen == data[-padlen:]:
        return data[:-padlen]
    else:
        return data

# Parser
def parse(data):
    parts = data.split(';')
    if len(parts) != 2:
        print('[!] Parsing Error')
        exit()
    else:
        return {'user':name, 'amount':int(amount)}

# Main Function
if __name__ == '__main__':
    print('=== Welcom to Trillion Bank ===')
    while True:
        option = input("Your option (1/2): ")
		if option == '1':
            name = input('Your name:')
            data = 'user:' + name + ';amount:10'
            print(aes.encrypt(pad(data.encode())).hex())
        else:
            session = input('Session:')
            session = bytes.fromhex(session)
            data = parse(unpad(aes.decrypt(session)).decode())
            print(f"Your account info: {data}")
            
            if data['amount'] > trillion:
                print(flag1)
            else:
                print("I don't have anything for you!")
```

## 解題
1. 觀察 source code，發現：
   - 把 `'user:' + [input] + ';amount:10'`  當成一組加密成 session 回來
   - 使用 `MODE_ECB` -> blocks 分開加密
   - Padding 以十六為單位 -> 一個 block 16 bytes
1. 設計使得加密內容剛好為 block 長度的倍數，
   ```
	   user:AAAAAAAAAAA ;amount:99999999 9999999999999999 amount:10
	   |___16 bytes___| |______________| |______________|
	        block 1	        block 2          block 3   
   ```
   --> 為了讓 amount > 1000000000000000000，blocks 數 = 3
	   -> session 取前 3 個 block = 48 個 bytes = 96 個字母（in 十六進制）
2. 寫腳本
   ```python
   from pwn import *

	HOST = "45.77.20.255"
	PORT = "31001"
	
	r = remote(HOST, PORT)
	r.recvline() # === Welcom to Trillion Bank ===
	
	def chooseOption(choice):
	    r.recvlines(3)
	    r.recv() # Your option (1/2):
	    r.sendline(str(choice).encode())
	    r.recv() # Your name:
	
	PAD_LEN = 16
	
	chooseOption(1)
	# 'user:'+name+';amount:10'
	payload = 'A'*(PAD_LEN-len('user:'))+';amount:'+'9'*(PAD_LEN-len(';amount:'))+'9'*(PAD_LEN)
	
	r.sendline(payload.encode())
	session = r.recvline().decode()[:96]
	
	chooseOption(2)
	r.sendline(session.encode())
	print(r.recv().decode().split('\n')[1])
   ```
   ![[W2-2_flag.png|643]]
3. flag = `FLAG{05aa82bb223ae4f57e320c7734f8d45f2f38659faf33f9043b6dfe0beeea5a93}`

