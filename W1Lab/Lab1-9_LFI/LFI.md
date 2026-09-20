#Web 

## 題目

**LFI**
給了一個網址，點開來
![[W1-9_web.png|583]]
## 解題
1. 觀察網頁
	- 點 Cappo 有提示："flag is in /var/www/html/flag.php"
	- php 含有 `include`，一般網頁是讀出檔案內容但不執行，`include` 會把指定檔案當成 PHP 程式的一部分載入並執行
2. 先嘗試 pathwalker 的做法，網址後面輸入 `?page=/../../../../../var/www/html/flag`，結果：
   ![[W1-9_noflag.png|169]]（呵呵...）
3. php 的 `include` 會直接把 `.php` 檔案直接執行，所以看不到原始碼 -> 利用 php 偽協議
   >[!abstract] php 偽協議
   >是 PHP 提供的一套特殊語法，可以用類似 URL 的格式來訪問及操作不同類型的資源
   >**常見協議**：
   >- `file://`：用於訪問本地檔案系統，ex: `include('file:///etc/passwd');`
   >- `php://`：用於訪問各個輸入/輸出流
   >	- `php://input`：讀取 POST 請求中的原始資料
   >	- `php://filter`：讀取檔案並進行轉換，ex: `include('php://filter/convert.base64-encode/resource=index.php');`
>- `data://` ：引入經過資料流包裝的資料

4. 要讀取網頁原始碼檔案 -> 後面輸入 
   ```
   ?page=php://filter/convert.base64-encode/resource=/../../../../../var/www/html/flag
   ```
   ![[W1-9_base64.png]]
5. 解碼，terminal 輸入：`echo "[字串]" | base64 -d`
   ![[W1-9_flag.png|622]]
6. flag = `CTF{lfi_3078f6cae51e0efe09b64494}`