#Web 

## 題目

**No Sql Injection**
給了一個網址，點開來
![[W1-25_web.png|433]]
`main` 簡化後：
```python
@app.route("/login", methods=["POST"])
def login():
    users = db.users
    username = request.json.get("username")
    password = request.json.get("password")

    user = users.find_one({"username": username, "password": password})

    if user:
        return jsonify(
            {
                "message": "Login successful",
                "secret": user.get("secret", "No secret found."),
            }
        )
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.before_first_request
def initialize_database():
    users = db.users

    # Insert default users
    guest_user = {"username": "guest", "password": "guest"}
    users.update_one({"username": "guest"}, {"$set": guest_user}, upsert=True)

    # Insert secret user
    secret_user = {
        "username": "admin",
        "password": b64encode(os.urandom(24)).decode("utf-8"),
        "secret": flag,
    }
    users.update_one({"username": "admin"}, {"$set": secret_user}, upsert=True)

```

### NoSQL
NoSQL（Not Only SQL）資料庫是一類非關聯型資料庫，不依賴固定的表格和欄位架構（例如 MongoDB、CouchDB、Redis ）[^1]
##### 常見類型：
1. **Document Store：** 使用 JSON 或 BSON 格式儲存文件，文件資料庫的結構靈活，Ex: MongoDB
2. **Key-Value Store：** 使用簡單的鍵值對來儲存資料，可以高效快速查詢，Ex: Redis 和 DynamoDB
3. **Graph Database：** 主要用於處理需要儲存關聯資料的應用，能夠有效查找和分析節點與節點之間的關係，Ex: MongoDB, Neo4j
4. **Column Store：** 使用資料行來儲存資料，適合處理大規模讀取和寫入的應用，Ex: Apache Cassandra 和 HBase 
##### 優勢
1. **靈活性：** 允許動態擴展資料模型，不需要預先定義的表結構
2. **水平擴展：** 可以透過增加更多的伺服器來處理大量的資料和請求
3. **高可用性和分佈式架構：** 大多數設計為分佈式系統，可以提供高可用性和容錯性，甚至在某些節點失效的情況下仍能保持系統運行
#### NoSQL injection
[^2]![[W1-25_NoSQL.svg|680]]
攻擊者透過操控<mark style="background: #FFF3A3A6;">未經妥善處理的查詢語法</mark>來改變應用程式的行為
通常發生在開發者未正確驗證或清理使用者輸入時
##### 類型
- **Syntax injection**: 破解 NoSQL 查詢語法，從而注入自訂惡意程式碼
- **Operator injection**: 使用 NoSQL 查詢運算子來操作查詢
##### MongoDB 查詢運算子
- `$where` - 滿足 JavaScript 表達式的文件
- `$ne` - 所有不等於指定值的欄位值
- `$in` - 欄位數值符合指定陣列中任何一個元素的資料，ex:
  ```SQL
  db.collection.find({ status: { $in: ["A", "D"] } })
  ```
- `$regex` - 選擇值與指定正規表示式相符的文件
##### 範例
- 在 JSON 訊息中，將查詢運算子（`"$ne":"invalid"`：所有不等於 "invalid" 的值）作為巢狀物件插入。例如， 
  ```json
  {"username":"wiener"}
  ``` 
  變成 
  ```json
  {"username":{"$ne":"invalid"}}
  ```
- 對於基於 URL 的輸入，透過 URL 參數插入查詢運算子。例如， `username=wiener` 變成 `username[$ne]=invalid`
---
## 解題
1. 觀察 source code，發現是用 json 格式存入 DB，並且有兩組預設帳密
   - guest / guest：沒有 secret
   - admin / base64(random)：有 secret = flag
   
   -> 目標：用 admin 的帳號獲取 secret
1. 用 Brup Suite 輔助觀察，先輸入 guest / guest 測試
   ![[W1-25_guest.png|626]]
2. 按右鍵 -> Send to Repeater
   ![[W1-25_send2repeate.png|425]]
   修改送出的 `username` 為 `admin`/`password` 部分為 `{"$ne":"x"}`（所有不等於 "x" 的值） 
   ![[W1-25_send.png|527]]
   送出
3. 得到 secret![[W1-25_flag.png|451]]
4. flag = `CTF{no_sql_injection_641b5538fa4fe15aa4b40dae}`











